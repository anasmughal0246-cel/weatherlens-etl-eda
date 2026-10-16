# Weather ETL + EDA Pipeline (Project 1)

Data: Open-Meteo API (free, no key). Cities: Lahore, Karachi, Islamabad.

## How to run
```
pip install -r requirements.txt
python pipeline.py    # Extract -> Transform (pandas + Pydantic) -> Load (SQLite)
python eda.py         # Exploratory data analysis, plots saved in figures/
```

## Files
- config.py     settings (cities, dates, paths)
- extract.py    gets data from the API
- schemas.py    Pydantic validation rules
- transform.py  cleans and validates data
- load.py       saves/reads SQLite database
- pipeline.py   runs the full ETL
- eda.py        analysis and plots

## For Project 2 and 3
```python
from load import read_all
df = read_all()
```