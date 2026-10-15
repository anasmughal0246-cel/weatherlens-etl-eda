"""Export weather.db to web/data.json so the Vercel website can use it.

Run this on your computer after pipeline.py:
    py export_data.py
"""
import json

from load import read_all

df = read_all()
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

data = {"cities": {}}
for city, g in df.groupby("city"):
    g = g.sort_values("date")
    data["cities"][city] = {
        "date": g["date"].tolist(),
        "tmean": g["temperature_2m_mean"].round(1).tolist(),
        "tmax": g["temperature_2m_max"].round(1).tolist(),
        "tmin": g["temperature_2m_min"].round(1).tolist(),
        "rain": g["precipitation_sum"].round(1).tolist(),
        "wind": g["wind_speed_10m_max"].round(1).tolist(),
    }

with open("web/data.json", "w") as f:
    json.dump(data, f, separators=(",", ":"))

print("Saved web/data.json with", len(df), "rows")