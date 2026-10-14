from load import read_all

df = read_all()

print(df.head(10))                           # pehli 10 rows
print(df.tail(5))                            # aakhri 5 rows
print(df.groupby("city").mean(numeric_only=True).round(2))   # har shehar ka average
print(df.nlargest(5, "temperature_2m_max")[["city", "date", "temperature_2m_max"]])  # 5 sab se garam din
print(df.nlargest(5, "precipitation_sum")[["city", "date", "precipitation_sum"]])    # 5 sab se zyada barish wale 
df.to_csv("weather_data.csv", index=False)