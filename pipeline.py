import pandas as pd

import config
from extract import extract
from load import load
from transform import transform

all_good = []
all_bad = []

for city, (lat, lon) in config.CITIES.items():
    print(f"Processing {city}...")
    raw = extract(city, lat, lon)
    good, bad = transform(city, raw)
    print(f"  valid rows: {len(good)}, rejected rows: {len(bad)}")
    all_good.append(good)
    all_bad.append(bad)

load(pd.concat(all_good, ignore_index=True), "daily_weather")

rejected = pd.concat(all_bad, ignore_index=True)
if not rejected.empty:
    load(rejected.astype(str), "rejected_rows")

print("Done! Data saved in", config.DB_PATH)