import altair as alt
import streamlit as st

import config

# On a fresh server the database does not exist yet, so build it first
if not config.DB_PATH.exists():
    import pipeline  # running this file creates weather.db

from load import read_all

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# One fixed colour per city, so a city looks the same in every chart
COLORS = {"Lahore": "#ef4444", "Karachi": "#0ea5e9", "Islamabad": "#22c55e"}
CITY_SCALE = alt.Scale(domain=list(COLORS.keys()), range=list(COLORS.values()))

st.set_page_config(page_title="WeatherLens", page_icon="🌦️", layout="wide")

# ---------- Custom style ----------
st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 55%, #22d3ee 100%);
        padding: 30px 36px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(29, 78, 216, 0.25);
    }
    .hero h1 { margin: 0; color: white; font-size: 2.4rem; }
    .hero p  { margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.92; }

    [data-testid="stMetric"] {
        background: white;
        padding: 16px 18px;
        border-radius: 16px;
        border-left: 6px solid #0ea5e9;
        box-shadow: 0 2px 12px rgba(15, 23, 42, 0.08);
    }
    [data-testid="stMetricLabel"] { color: #475569; }
    [data-testid="stMetricValue"] { color: #0f172a; }

    .stTabs [data-baseweb="tab"] { font-size: 1.05rem; padding: 10px 18px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    df = read_all()
    df["year"] = df["date"].dt.year
    df["month_name"] = df["month"].apply(lambda m: MONTHS[m - 1])
    return df


df = get_data()

# ---------- Banner ----------
st.markdown(
    """
    <div class="hero">
        <h1>🌦️ WeatherLens</h1>
        <p>Explore daily weather of Pakistani cities &nbsp;|&nbsp; Data: Open-Meteo API</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar filters ----------
st.sidebar.title("🔎 Filters")
all_cities = list(df["city"].unique())
cities = st.sidebar.multiselect("Cities", all_cities, default=all_cities)
min_year, max_year = int(df["year"].min()), int(df["year"].max())
years = st.sidebar.slider("Years", min_year, max_year, (min_year, max_year))
st.sidebar.caption("Change filters and every chart updates.")

df = df[df["city"].isin(cities) & df["year"].between(years[0], years[1])]

if df.empty:
    st.warning("No data for these filters. Please select at least one city.")
    st.stop()

# ---------- Key numbers ----------
hottest = df.loc[df["temperature_2m_max"].idxmax()]

c1, c2, c3, c4 = st.columns(4)
c1.metric("📅 Days of data", f"{len(df):,}")
c2.metric("🌡️ Average temperature", f"{df['temperature_2m_mean'].mean():.1f} °C")
c3.metric("🔥 Hottest day", f"{hottest['temperature_2m_max']:.1f} °C",
          f"{hottest['city']}, {hottest['date']:%d %b %Y}", delta_color="off")
c4.metric("☔ Rainy days", f"{df['is_rainy'].mean() * 100:.1f} %")

st.write("")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🌡️ Temperature", "🌧️ Rainfall", "🏙️ City comparison", "📄 Data"]
)

# --- Temperature ---
with tab1:
    st.subheader("Temperature over time (30-day average)")
    trend = df.sort_values("date").copy()
    trend["average"] = trend.groupby("city")["temperature_2m_mean"].transform(
        lambda s: s.rolling(30).mean()
    )
    line = alt.Chart(trend.dropna(subset=["average"])).mark_line(strokeWidth=2.5).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("average:Q", title="Temperature (°C)", scale=alt.Scale(zero=False)),
        color=alt.Color("city:N", scale=CITY_SCALE, title="City"),
        tooltip=["city", "date:T", alt.Tooltip("average:Q", format=".1f")],
    ).properties(height=350, width="container").interactive()
    st.altair_chart(line)

    left, right = st.columns(2)

    with left:
        st.subheader("Average temperature by month")
        monthly = df.groupby(["city", "month_name"])["temperature_2m_mean"].mean().reset_index()
        bars = alt.Chart(monthly).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X("month_name:N", sort=MONTHS, title="Month"),
            y=alt.Y("temperature_2m_mean:Q", title="Temperature (°C)"),
            color=alt.Color("city:N", scale=CITY_SCALE, title="City"),
            xOffset="city:N",
            tooltip=["city", "month_name", alt.Tooltip("temperature_2m_mean:Q", format=".1f")],
        ).properties(height=320, width="container")
        st.altair_chart(bars)

    with right:
        st.subheader("Heatmap: month vs year")
        heat = df.groupby(["year", "month_name"])["temperature_2m_mean"].mean().reset_index()
        heatmap = alt.Chart(heat).mark_rect().encode(
            x=alt.X("month_name:N", sort=MONTHS, title="Month"),
            y=alt.Y("year:O", title="Year"),
            color=alt.Color("temperature_2m_mean:Q", title="°C",
                            scale=alt.Scale(scheme="redyellowblue", reverse=True)),
            tooltip=["year", "month_name", alt.Tooltip("temperature_2m_mean:Q", format=".1f")],
        ).properties(height=320, width="container")
        st.altair_chart(heatmap)

# --- Rainfall ---
with tab2:
    st.subheader("Average rainfall by month")
    rain = df.groupby("month_name")["precipitation_sum"].mean().reset_index()
    rain_chart = alt.Chart(rain).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X("month_name:N", sort=MONTHS, title="Month"),
        y=alt.Y("precipitation_sum:Q", title="Rainfall (mm/day)"),
        color=alt.Color("precipitation_sum:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=["month_name", alt.Tooltip("precipitation_sum:Q", format=".2f")],
    ).properties(height=350, width="container")
    st.altair_chart(rain_chart)

    st.subheader("Top 5 rainiest days")
    top_rain = df.nlargest(5, "precipitation_sum")[["city", "date", "precipitation_sum"]]
    top_rain["date"] = top_rain["date"].dt.strftime("%d %b %Y")
    top_rain.columns = ["City", "Date", "Rainfall (mm)"]
    st.dataframe(top_rain, hide_index=True)

# --- City comparison ---
with tab3:
    st.subheader("Summary by city")
    summary = df.groupby("city").agg(
        avg_temp=("temperature_2m_mean", "mean"),
        max_temp=("temperature_2m_max", "max"),
        min_temp=("temperature_2m_min", "min"),
        avg_rain=("precipitation_sum", "mean"),
        rainy_days_pct=("is_rainy", "mean"),
    )
    summary["rainy_days_pct"] = summary["rainy_days_pct"] * 100
    summary.columns = ["Avg temp (°C)", "Max temp (°C)", "Min temp (°C)",
                       "Avg rain (mm/day)", "Rainy days (%)"]
    st.dataframe(summary.round(2))

    st.subheader("Temperature spread by city")
    box = alt.Chart(df).mark_boxplot(extent="min-max").encode(
        x=alt.X("city:N", title="City"),
        y=alt.Y("temperature_2m_mean:Q", title="Temperature (°C)"),
        color=alt.Color("city:N", scale=CITY_SCALE, legend=None),
    ).properties(height=350, width="container")
    st.altair_chart(box)

# --- Data ---
with tab4:
    st.subheader("Data")
    st.dataframe(df, hide_index=True)
    st.download_button(
        "⬇️ Download as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="weather_data.csv",
        mime="text/csv",
    )

st.divider()
st.caption("WeatherLens | Project 1: ETL + EDA Pipeline")