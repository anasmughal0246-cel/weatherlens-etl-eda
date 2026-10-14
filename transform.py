import pandas as pd
from pydantic import ValidationError

from schemas import DailyWeather


def transform(city, raw):
    """Turn raw JSON into a clean DataFrame. Returns (good_rows, bad_rows)."""
    df = pd.DataFrame(raw["daily"])
    df = df.rename(columns={"time": "date"})
    df["city"] = city

    good = []
    bad = []
    for row in df.to_dict("records"):
        # NaN -> None so Pydantic accepts missing values
        row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
        try:
            good.append(DailyWeather(**row).model_dump())
        except ValidationError as error:
            row["error"] = str(error)
            bad.append(row)

    good_df = pd.DataFrame(good)
    bad_df = pd.DataFrame(bad)

    # extra columns that will be useful in Project 2 and 3
    good_df["date"] = pd.to_datetime(good_df["date"])
    good_df["month"] = good_df["date"].dt.month
    good_df["is_rainy"] = (good_df["precipitation_sum"] >= 1).astype(int)

    return good_df, bad_df