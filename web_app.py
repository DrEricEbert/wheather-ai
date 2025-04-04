# web_app.py

import streamlit as st
import torch
import numpy as np
from model import WeatherForecaster
from train import load_model
from data_loader import load_dwd_weather_data
from sklearn.preprocessing import StandardScaler

st.title("🌦️ Wetter-KI Vorhersage (DWD)")

station_id = st.text_input("Station-ID (z. B. 01048)", "01048")
days = st.slider("Tage vorhersagen", 1, 7, 3)

if st.button("Vorhersage starten"):
    df = load_dwd_weather_data(station_id, years=1)
    if len(df) < 24:
        st.error("Nicht genug Daten für Vorhersage.")
    else:
        df_last = df.tail(24)
        features = ["temperature", "humidity", "wind_speed", "season", "hour"]
        scaler = StandardScaler()
        X = scaler.fit_transform(df_last[features])

        model = WeatherForecaster(input_size=5, hidden_size=64)
        load_model(model, "models/forecaster.pt")

        preds = []
        for _ in range(days):
            X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                pred = model(X_tensor).item()
            preds.append(pred)
            new_row = [pred, 50, 5, 1, (X[-1, 4] + 1) % 24]
            X = np.vstack([X[1:], new_row])
        st.line_chart(preds)