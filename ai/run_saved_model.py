import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import joblib
import keras
import json

from lstm import read_input_data

SEQ_LEN = 24  # 24 Hours
SAVED_MODEL_PATH = "saved/model.keras"
SAVED_X_SCALER = "saved/X_scaler.pkl"
SAVED_Y_SCALER = "saved/y_scaler.pkl"

# Matches features used during training
FEATURE_COLUMNS = [
    "lat1", "long1", "elev1", "temp1", "pressure1",
    "lat2", "long2", "elev2", "temp2", "pressure2",
    "temperature_2m_x_delta_3h", "temperature_2m_y_delta_3h",
    "surface_pressure_x_delta_3h", "surface_pressure_y_delta_3h",
    "PGF_x", "PGF_y", "PGF_magnitude"
    # "coast_dist"
]

def plot_prediction(dates, prediction):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prediction, label="Predicted Wind Speed")
    plt.title("Predicted Wind Speed")
    plt.xlabel("Date")
    plt.ylabel("Wind Speed (km/h)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load preprocessed input
    df = read_input_data("./input/result.json")  # Includes PGF + deltas
    df.dropna(inplace=True)

    # Store dates
    dates = pd.to_datetime(df["date"])
    trimmed_dates = dates.iloc[SEQ_LEN:]

    # Load scalers
    X_scaler = joblib.load(SAVED_X_SCALER)
    y_scaler = joblib.load(SAVED_Y_SCALER)

    # Prepare and scale inputs
    scaled = X_scaler.transform(df[FEATURE_COLUMNS])

    X = []
    for i in range(SEQ_LEN, len(scaled)):
        X.append(scaled[i - SEQ_LEN:i])
    X = np.array(X)

    # Load model and predict
    model = keras.models.load_model(SAVED_MODEL_PATH)
    y_pred_scaled = model.predict(X).flatten()
    y_pred_unscaled = y_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

    # Save output
    with open("output/prediction.json", "w") as f:
        json.dump({
            "dates": trimmed_dates.astype(str).to_list(),
            "predictions": y_pred_unscaled.tolist()
        }, f, indent=4)

    # Plot
    plot_prediction(trimmed_dates, y_pred_unscaled)
