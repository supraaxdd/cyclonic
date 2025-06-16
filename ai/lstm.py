import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
import joblib

from pandas import DataFrame

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

from keras.src.models import Sequential
from keras.src.layers import LSTM, Dense, Dropout
from keras.src.optimizers import RMSprop
from keras.src.callbacks import EarlyStopping

SEQUENCE_LENGTH = 24  # 24 hours
SAVED_MODEL_PATH = "saved/model.keras"
SAVED_X_SCALER = "saved/X_scaler.pkl"
SAVED_Y_SCALER = "saved/y_scaler.pkl"

def read_input_data(input_set: str):
    file_path = Path(Path.cwd(), input_set)
    return pd.read_json(file_path)

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

def build_model(X, y) -> Sequential:
    # Define LSTM model
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.3),
        LSTM(64),
        Dropout(0.3),
        Dense(1)
    ])

    # Define the optimizer for the LSTM
    optimizer = RMSprop(learning_rate=0.005, momentum=0.05)

    model.compile(optimizer=optimizer, loss='mse')
    model.summary()

    return model

def predict_wind_speed_lstm(features: pd.DataFrame, targets: pd.DataFrame):
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

    model = build_model(X, y)

    # Train
    model.fit(
        X_train, y_train,
        epochs=200,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=1,
        callbacks=[early_stop]
    )

    model.save(Path(SAVED_MODEL_PATH))

    # Predict and unscale
    y_pred_scaled = model.predict(X_test)
    y_pred = y_scaler.inverse_transform(y_pred_scaled)
    y_test_unscaled = y_scaler.inverse_transform(y_test.reshape(-1, 1))

    # Evaluate
    print(f"\nLSTM Model Evaluation:")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_scaled)):.4f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred_scaled):.4f}")

    plot_lstm_results(y_test_unscaled, y_pred)

if __name__ == "__main__":
    df = read_input_data("./input/result.json")  # Already includes PGF and deltas
    features, targets = get_vectors(df)

    predict_wind_speed_lstm(features, targets)