# 🌦️ Wetter-KI mit DWD-Daten (PyTorch + PySide6 + Streamlit)

Ein Projekt zur Wettervorhersage auf Basis von 10 Jahren DWD-Daten, mit Deep Learning (LSTM), GUI und Web-App.

## 🔧 Installation

```bash
git clone https://github.com/dein-nutzername/weather-ai.git
cd weather-ai
pip install -r requirements.txt
```

## 🚀 Starten
* GUI (PySide6)

```python main.py```

* Web-App (Streamlit)

```streamlit run web_app.py```

## 📦 Funktionen

* DWD-Stationen auswählen
* Daten laden (10 Jahre)
* LSTM trainieren (Temperatur)
* Vorhersage: 1 Tag oder 7 Tage
* Matplotlib-Visualisierung
* Automatisches Modell-Laden
