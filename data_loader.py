# data_loader.py

from wetterdienst.provider.dwd.observation import DwdObservationRequest
from wetterdienst import Settings

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def load_dwd_weather_data(station_id="01048", years=10):
    settings = Settings(ts_skip_empty=True, ts_skip_criteria="min", ignore_env=True)
    karlsruhe = (49.19780976647141, 8.135207205143768)
    request = DwdObservationRequest(
    parameters=[("daily", "kl"), ("daily", "solar")],
    start_date="2021-01-01",
    end_date="2021-12-31",
    settings=settings,
    )
    stations = request.filter_by_rank(latlon=karlsruhe, rank=2)
    values = stations.values.all()
    print(values.df.head())


    stations = request.filter_by_station_id(station_id).values.query()
    df = pd.concat([s.df for s in stations])

    df = df[df["date"] > datetime.utcnow() - timedelta(days=365*years)]
    df = df.pivot(index="date", columns="parameter", values="value").reset_index()
    df = df.rename(columns={
        "temperature_air_mean_200": "temperature",
        "humidity": "humidity",
        "wind_speed": "wind_speed"
    })
    df = df.dropna()
    df["month"] = df["date"].dt.month
    df["season"] = df["month"] % 12 // 3
    df["hour"] = df["date"].dt.hour
    return df

def get_station_list():
   # settings = Settings(ts_skip_empty=True, ts_skip_criteria="min", ignore_env=True)
    request = DwdObservationRequest(
    parameters=[("daily", "wl")],
    start_date="2014-01-01",
    end_date="2024-12-31",
    #settings=settings,
    )
    stations = request.filter_by_name("Rostock").all().df
    #stations = DwdObservationStations(resolution="hourly").all().df
    stations = stations.dropna(subset=["station_id", "name"])
    station_list = [(f"{row['name']} ({row['station_id']})", row["station_id"]) for _, row in stations.iterrows()]
    return station_list[:100]