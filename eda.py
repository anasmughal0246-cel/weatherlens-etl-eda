import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import config
from load import read_all

config.FIG_DIR.mkdir(exist_ok=True)
df = read_all()

# 1. Basic info
print("Shape:", df.shape)
print("\nRows per city:\n", df["city"].value_counts())
print("\nMissing values:\n", df.isna().sum())
print("\nSummary statistics:\n", df.describe().round(2))

# 2. Temperature distribution
df["temperature_2m_mean"].hist(bins=40)
plt.title("Temperature distribution")
plt.xlabel("Mean temperature (C)")
plt.ylabel("Temperature (C)")   # graph 3
plt.ylabel("Rainfall (mm/day)") # graph 4
plt.savefig(config.FIG_DIR / "1_temperature_distribution.png")
plt.close()

# 3. Temperature over time for each city
for city, group in df.groupby("city"):
    plt.plot(group["date"], group["temperature_2m_mean"].rolling(30).mean(), label=city)
plt.title("Temperature over time (30-day average)")
plt.legend()
plt.savefig(config.FIG_DIR / "2_temperature_over_time.png")
plt.close()

# 4. Average temperature by month
df.groupby("month")["temperature_2m_mean"].mean().plot(kind="bar")
plt.title("Average temperature by month")
plt.savefig(config.FIG_DIR / "3_temperature_by_month.png")
plt.close()

# 5. Average rainfall by month
df.groupby("month")["precipitation_sum"].mean().plot(kind="bar")
plt.title("Average rainfall by month")
plt.savefig(config.FIG_DIR / "4_rainfall_by_month.png")
plt.close()

# 6. Correlation between numeric columns
print("\nCorrelation:\n", df.drop(columns=["city", "date"]).corr().round(2))

print("\nPlots saved in", config.FIG_DIR)