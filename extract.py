import requests

import config


def extract(city, lat, lon):
    """Download daily weather for one city from the API and return it as JSON (dict)."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": config.START_DATE,
        "end_date": config.END_DATE,
        "daily": ",".join(config.DAILY_VARS),
        "timezone": "Asia/Karachi",
    }
    response = requests.get(config.API_URL, params=params, timeout=60)
    response.raise_for_status()
    return response.json()