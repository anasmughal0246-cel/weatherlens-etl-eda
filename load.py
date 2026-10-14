import sqlite3

import pandas as pd

import config


def load(df, table="daily_weather"):
    """Save a DataFrame into the SQLite database (replaces the table)."""
    conn = sqlite3.connect(config.DB_PATH)
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()


def read_all(table="daily_weather"):
    """Read the table back as a DataFrame. Use this in Project 2 and 3."""
    conn = sqlite3.connect(config.DB_PATH)
    df = pd.read_sql(f"SELECT * FROM {table}", conn, parse_dates=["date"])
    conn.close()
    return df