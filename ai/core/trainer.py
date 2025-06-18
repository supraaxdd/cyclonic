import joblib

from pathlib import Path

from utils.data import read_input_data, create_folder_if_not_exists

from keras.src.models import Sequential
from keras.src.layers import LSTM, Dense, Dropout
from keras.src.optimizers import RMSprop, Adam
from keras.src.callbacks import EarlyStopping

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SEQUENCE_LENGTH = 24  # 24 hours
SAVED_FOLDER_PATH = "saved"
SAVED_MODEL_PATH = "saved/model.keras"
SAVED_X_SCALER = "saved/X_scaler.pkl"
SAVED_Y_SCALER = "saved/y_scaler.pkl"

def get_vectors(df: pd.DataFrame):
    targets = df[["date", "wind_speed_10m_x"]]
    features = df.drop(columns=["wind_speed_10m_x"])
    
    return features, targets

def plot_lstm_results(y_true, y_pred):
    plt.figure(figsize=(10, 5))

    plt.plot(y_true, label="Actual", linewidth=1)
    plt.plot(y_pred, label="Predicted", linewidth=1, linestyle='--')

    plt.title("Wind Speed Prediction with LSTM")

    plt.xlabel("Time Steps")
    plt.ylabel("Wind Speed (km/h)")

    plt.legend()

    plt.tight_layout()

    plt.show()

def build_model(X, optimizer_name: str, lr: float, dropout: float) -> Sequential:
    optimizers = {
        "rmsprop": RMSprop,
        "adam": Adam
    }

    optimizer_class = optimizers.get(optimizer_name)
    if not optimizer_class:
        raise ValueError(f"Unsupported optimizer: {optimizer_name}")
    
    # Define LSTM model
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(dropout),
        LSTM(64),
        Dropout(dropout),
        Dense(1)
    ])

    # Define the optimizer for the LSTM
    optimizer = optimizer_class(learning_rate=lr)

    model.compile(optimizer=optimizer, loss='mse') # type: ignore
    model.summary()

    return model

def train(epochs: int, lr: float, dropout: float, optimizer_name: str, no_plotting: bool) -> dict:
    df = read_input_data("./input/result.json")
    features, targets = get_vectors(df)

    df = features.copy()

    df["wind_speed_10m_x"] = targets["wind_speed_10m_x"].values
    df.dropna(inplace=True)

    # FEATURE_COLUMNS = [
    #     "temperature_2m", "temperature_80m", "temperature_120m", "temperature_180m",
    #     "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm",
    #     "pressure", "pressure_delta_3h", "temperature_2m_delta_3h",
    #     "PGF_x", "PGF_y", "PGF_magnitude"
    # ]

    FEATURE_COLUMNS = [
            "lat1", "long1", "elev1", "temp1", "pressure1",
            "lat2", "long2", "elev2", "temp2", "pressure2",
            "temperature_2m_x_delta_3h", "temperature_2m_y_delta_3h",
            "surface_pressure_x_delta_3h", "surface_pressure_y_delta_3h",
            "PGF_x", "PGF_y", "PGF_magnitude"
            # "coast_dist"
    ]

    create_folder_if_not_exists(SAVED_FOLDER_PATH)

    # Fit and save X-scaler
    X_scaler = StandardScaler()
    scaled_X = X_scaler.fit_transform(df[FEATURE_COLUMNS])
    joblib.dump(X_scaler, SAVED_X_SCALER)

    # Fit and save y-scaler
    y_scaler = StandardScaler()
    scaled_y = y_scaler.fit_transform(df[["wind_speed_10m_x"]])
    joblib.dump(y_scaler, SAVED_Y_SCALER)

    # Creating a snapshot of each hour to be predicted based on the previous 24 hours of data
    # for the time-series model
    X, y = [], []
    for i in range(SEQUENCE_LENGTH, len(scaled_X)):
        X.append(scaled_X[i - SEQUENCE_LENGTH:i]) # Snapshot of the input data over the last 24 hours for a given period
        y.append(scaled_y[i][0]) # Compliling what the wind is looking like at this moment (speed and direction)

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Define a callback to discontinue model training if no further improvements are found
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True
    )

    model = build_model(X, optimizer_name, lr, dropout)

    # Train
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=1, # type: ignore
        callbacks=[early_stop]
    )

    model.save(Path(SAVED_MODEL_PATH))

    # Predict and unscale
    y_pred_scaled = model.predict(X_test)
    y_pred = y_scaler.inverse_transform(y_pred_scaled)
    y_test_unscaled = y_scaler.inverse_transform(y_test.reshape(-1, 1))

    # Evaluate
    mse = mean_squared_error(y_test, y_pred_scaled)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred_scaled)
    r2 = r2_score(y_test, y_pred_scaled)
    val_loss = history.history["val_loss"][-1]

    print(f"\nLSTM Model Evaluation:")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")

    if not no_plotting:
        plot_lstm_results(y_test_unscaled, y_pred)

    return {
        "mse": mse,
        "rmse": rmse,
        "mae": mae,
        "val_loss": val_loss,
        "r2": r2
    }