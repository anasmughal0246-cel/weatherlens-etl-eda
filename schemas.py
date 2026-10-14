from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class DailyWeather(BaseModel):
    city: str
    date: date
    temperature_2m_max: Optional[float] = Field(None, ge=-60, le=60)
    temperature_2m_min: Optional[float] = Field(None, ge=-60, le=60)
    temperature_2m_mean: Optional[float] = Field(None, ge=-60, le=60)
    precipitation_sum: Optional[float] = Field(None, ge=0)
    wind_speed_10m_max: Optional[float] = Field(None, ge=0)