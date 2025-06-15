from math import radians, sin, cos, sqrt, asin
from pandas import DataFrame

def haversine(lat1: float, long1: float, lat2: float, long2: float):
    """
    Calculates the distance between two points on Earth using the haversine formula\n
    :param lat1: The latitude co-ordinate of the first location\n
    :param long1: The longitude co-ordinate of the first location\n
    :param lat2: The latitude co-ordinate of the second location\n
    :param long2: The longitude co-ordinate of the second location\n
    """
    R = 6371

    rlat1 = radians(lat1)
    rlat2 = radians(lat2)

    dlat = radians(lat2 - lat1)
    dlong = radians(long2 - long1)

    a = (sin(dlat / 2)**2) + cos(rlat1) * cos(rlat2) * (sin(dlong / 2)**2)

    d = 2 * R * asin(sqrt(a))

    return d

def calculate_air_density(temp_c: float, pavg: float):
    """
    temp_c = Temperature (°C)\n
    pavg = The average pressure between the two points (Pa)
    """
    rd = 287.05  # Gas constant for dry air
    kelvin = temp_c + 273.15
    return pavg / (rd * kelvin)

def calculate_distance(x: tuple, y: tuple):
    """
    Returns dy and dx in meters between two (lat, lon) points
    """
    lat_x, lon_x = x
    lat_y, lon_y = y

    deg_to_m_lat = 111000  # meters per degree latitude
    avg_lat_rad = radians((lat_x + lat_y) / 2)
    deg_to_m_lon = 111000 * cos(avg_lat_rad)

    dx = (lon_y - lon_x) * deg_to_m_lon  # East-West
    dy = (lat_y - lat_x) * deg_to_m_lat  # North-South

    return dy, dx

def calculate_pgf_components(dy: float, dx: float, pd: float, rho: float):
    """
    Calculates the PGF vector components given dy, dx, pressure delta, and air density
    """
    r = sqrt(dx**2 + dy**2)
    dP_dx = pd / r * (dx / r)
    dP_dy = pd / r * (dy / r)

    F_x = -1 / rho * dP_dx
    F_y = -1 / rho * dP_dy
    return F_y, F_x  # (dy, dx) for consistency

def calculate_pgf_time_series(merged_df: DataFrame) -> DataFrame:
    loc1 = (merged_df["lat_x"].iloc[0], merged_df["long_x"].iloc[0])
    loc2 = (merged_df["lat_y"].iloc[0], merged_df["long_y"].iloc[0])
    dy, dx = calculate_distance(loc2, loc1)

    pgf_data = {
        "PGF_x": [],
        "PGF_y": [],
        "PGF_magnitude": []
    }

    for i, row in merged_df.iterrows():
        try:
            temp_c = float(row["temperature_2m_x"])
            p1 = float(row["surface_pressure_y"])
            p2 = float(row["surface_pressure_x"])
            pd_val = p2 - p1
            pavg_val = (p1 + p2) / 2
            rho = calculate_air_density(temp_c, pavg_val)
            Fy, Fx = calculate_pgf_components(dy, dx, pd_val, rho)
            magnitude = sqrt(Fx**2 + Fy**2)
        except Exception:
            Fx, Fy, magnitude = 0.0, 0.0, 0.0

        pgf_data["PGF_x"].append(Fx)
        pgf_data["PGF_y"].append(Fy)
        pgf_data["PGF_magnitude"].append(magnitude)

    return DataFrame(pgf_data)
