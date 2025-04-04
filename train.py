# train.py

import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
import os

class WeatherDataset(Dataset):
    def __init__(self, df, sequence_length=24, task="regression"):
        self.sequence_length = sequence_length
        features = ["temperature", "humidity", "wind_speed", "season", "hour"]
        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(df[features].values)
        self.y = df["temperature"].values
        self.task = task

    def __len__(self):
        return len(self.X) - self.sequence_length

    def __getitem__(self, idx):
        x = self.X[idx:idx+self.sequence_length]
        y = self.y[idx+self.sequence_length]
        x = torch.tensor(x, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32)
        return x, y

def train_model(model, dataset, task="regression", epochs=5, lr=0.001, batch_size=64):
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        total_loss = 0
        for X, y in loader:
            out = model(X).squeeze()
            loss = criterion(out, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[Epoch {epoch+1}] Loss: {total_loss/len(loader):.4f}")

    save_model(model, "models/forecaster.pt")

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path)

def load_model(model, path):
    if os.path.exists(path):
        model.load_state_dict(torch.load(path))
        print(f"✅ Modell geladen aus {path}")
    else:
        print(f"⚠️ Modell-Datei {path} nicht gefunden.")