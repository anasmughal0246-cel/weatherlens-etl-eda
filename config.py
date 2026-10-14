from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "weather.db"
FIG_DIR = ROOT / "figures"

API_URL = "https://archive-api.open-meteo.com/v1/archive"

# city: (latitude, longitude)
CITIES = {
    "Lahore": (31.5204, 74.3587),
    "Karachi": (24.8607, 67.0011),
    "Islamabad": (33.6844, 73.0479),
}

START_DATE = "2020-01-01"
END_DATE = "2025-12-31"

DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
]