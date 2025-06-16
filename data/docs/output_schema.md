# Cyclonic Output File Schema (Flat Forecast Vector)

## 📄 File Format
JSON — list of records (one per hour)

## 🧾 Example Record
```json
{
    "date": "2025-06-16T03:00:00Z",
    "lat1": 51.844127655,
    "long1": -8.4870300293,
    "elev1": 142.0,
    "temp1": 10.5874996185,
    "pressure1": 1010.0119628906,
    "wind_speed_10m_x": 10.0799999237,
    "lat2": 52.1761741638,
    "long2": -9.5157928467,
    "elev2": 28.0,
    "temp2": 10.7929992676,
    "pressure2": 1023.3477783203,
    "temperature_2m_x_delta_3h": -1.0500001907,
    "temperature_2m_y_delta_3h": -0.7000007629,
    "surface_pressure_x_delta_3h": -0.5547485352,
    "surface_pressure_y_delta_3h": -0.7064208984,
    "PGF_x": 0.0119214484,
    "PGF_y": -0.0062512837,
    "PGF_magnitude": 0.0134610356
}
```

## 🔍 Field Descriptions

| Field | Description |
|-------|-------------|
| `date` | ISO timestamp of the forecasted hour |
| `lat1`, `long1`, `elev1` | Geographic coordinates and elevation of Location 1 |
| `temp1`, `pressure1` | Temperature and pressure at Location 1 |
| `wind_speed_10m_x` | Wind speed at 10m for Location 1 |
| `lat2`, `long2`, `elev2` | Geographic coordinates and elevation of Location 2 |
| `temp2`, `pressure2` | Temperature and pressure at Location 2 |
| `temperature_2m_x_delta_3h` | 3-hour temperature delta at Location 1 |
| `temperature_2m_y_delta_3h` | 3-hour temperature delta at Location 2 |
| `surface_pressure_x_delta_3h` | 3-hour surface pressure delta at Location 1 |
| `surface_pressure_y_delta_3h` | 3-hour surface pressure delta at Location 2 |
| `PGF_x`, `PGF_y` | Pressure gradient force components in the x/y direction |
| `PGF_magnitude` | Total PGF magnitude derived from x/y components |

## Notes
- All fields are numeric (float), except `date` which is string.
- Data is pre-aligned for direct use in time-series or supervised learning models.
- Values are standardized in SI-compatible units (e.g. pressure in hPa, distance in degrees/meters where applicable).
- PGF is derived from horizontal pressure differences and may be unit-normalized depending on model spec.