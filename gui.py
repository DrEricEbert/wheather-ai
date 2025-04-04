# gui.py

from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QFormLayout,
    QMessageBox, QFileDialog, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import torch
import numpy as np

from model import WeatherForecaster
from train import train_model, load_model, WeatherDataset
from data_loader import load_dwd_weather_data, get_station_list
from sklearn.preprocessing import StandardScaler

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌤️ Wetter-KI Vorhersage (DWD)")
        self.resize(500, 700)
        self.df = None
        self.model = None

        layout = QVBoxLayout()
        form = QFormLayout()

        # Station auswählen
        self.station_combo = QComboBox()
        for name, sid in get_station_list():
            self.station_combo.addItem(name, sid)
        form.addRow("DWD Station:", self.station_combo)

        # Hyperparameter
        self.lr_input = QLineEdit("0.001")
        self.epoch_input = QLineEdit("5")
        self.hidden_input = QLineEdit("64")
        form.addRow("Lernrate:", self.lr_input)
        form.addRow("Epochen:", self.epoch_input)
        form.addRow("LSTM Hidden Size:", self.hidden_input)

        # Eingabefelder für Prognose
        self.temp_input = QLineEdit()
        self.hum_input = QLineEdit()
        self.wind_input = QLineEdit()
        self.season_input = QLineEdit()
        self.hour_input = QLineEdit()
        form.addRow("Temp (°C):", self.temp_input)
        form.addRow("Feuchte (%):", self.hum_input)
        form.addRow("Wind (m/s):", self.wind_input)
        form.addRow("Jahreszeit (0-3):", self.season_input)
        form.addRow("Stunde (0-23):", self.hour_input)

        layout.addLayout(form)

        # Buttons
        self.load_btn = QPushButton("🔄 Daten laden")
        self.train_btn = QPushButton("🧠 Trainieren")
        self.predict_btn = QPushButton("📈 1-Tages-Vorhersage")
        self.predict_multi_btn = QPushButton("📆 Mehrtages-Vorhersage")
        layout.addWidget(self.load_btn)
        layout.addWidget(self.train_btn)
        layout.addWidget(self.predict_btn)
        layout.addWidget(self.predict_multi_btn)

        # Canvas
        self.canvas = MplCanvas(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Events
        self.load_btn.clicked.connect(self.load_data)
        self.train_btn.clicked.connect(self.train_model)
        self.predict_btn.clicked.connect(self.predict_once)
        self.predict_multi_btn.clicked.connect(self.predict_next_days)

        # Modell automatisch laden
        self.model = WeatherForecaster(input_size=5, hidden_size=64)
        load_model(self.model, "models/forecaster.pt")

    def load_data(self):
        station_id = self.station_combo.currentData()
        self.df = load_dwd_weather_data(station_id=station_id)
        QMessageBox.information(self, "Info", f"{len(self.df)} Wetterdaten geladen.")

    def train_model(self):
        if self.df is None:
            return QMessageBox.warning(self, "Fehler", "Zuerst Daten laden.")
        lr = float(self.lr_input.text())
        epochs = int(self.epoch_input.text())
        hidden = int(self.hidden_input.text())
        self.model = WeatherForecaster(input_size=5, hidden_size=hidden)
        dataset = WeatherDataset(self.df, task="regression")
        train_model(self.model, dataset, task="regression", epochs=epochs, lr=lr)
        QMessageBox.information(self, "Fertig", "Modell trainiert.")

    def predict_once(self):
        try:
            inputs = [
                float(self.temp_input.text()),
                float(self.hum_input.text()),
                float(self.wind_input.text()),
                int(self.season_input.text()),
                int(self.hour_input.text())
            ]
            X = torch.tensor([inputs]*24, dtype=torch.float32).unsqueeze(0)
            self.model.eval()
            with torch.no_grad():
                pred = self.model(X).item()
            QMessageBox.information(self, "Vorhersage", f"Vorhergesagte Temp: {pred:.2f} °C")
        except Exception as e:
            QMessageBox.warning(self, "Fehler", str(e))

    def predict_next_days(self, days=7):
        if self.df is None:
            QMessageBox.warning(self, "Fehler", "Daten fehlen.")
            return
        df_last = self.df.tail(24)
        scaler = StandardScaler()
        features = ["temperature", "humidity", "wind_speed", "season", "hour"]
        X = scaler.fit_transform(df_last[features])
        preds = []
        for _ in range(days):
            X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                pred = self.model(X_tensor).item()
            preds.append(pred)
            new_row = [pred, 50, 5, 1, (X[-1, 4] + 1) % 24]
            X = np.vstack([X[1:], new_row])
        self.plot_prediction(preds)

    def plot_prediction(self, preds):
        self.canvas.axes.clear()
        self.canvas.axes.plot(preds, label="Vorhersage", color="blue")
        self.canvas.axes.set_title("Vorhersage (nächste Tage)")
        self.canvas.axes.legend()
        self.canvas.draw()