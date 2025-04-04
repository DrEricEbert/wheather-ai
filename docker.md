
## ✅ Docker-Container für **Streamlit Web-App**

### 📄 `Dockerfile`

```dockerfile
# Basis-Image mit Python
FROM python:3.10-slim

# Installiere System-Abhängigkeiten
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Kopiere Projektdateien
COPY . /app

# Installiere Python-Abhängigkeiten
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponiere Port für Streamlit
EXPOSE 8501

# Starte die Streamlit-App
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📦 Optional: `.dockerignore` (für saubere Builds)

```dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
models/
*.pt
*.log
*.DS_Store
```

---

## 🧪 Beispiel: Container bauen und starten

### 1. 📦 Docker-Image bauen

```bash
docker build -t weather-ai .
```

### 2. ▶️ Container starten

```bash
docker run -p 8501:8501 weather-ai
```

### 3. 🌐 App öffnen

Gehe zu: [http://localhost:8501](http://localhost:8501)

---

## 🔁 Für automatisches Modell-Download (optional)

Falls du das Modell beim Start automatisch herunterladen möchtest, kannst du in `web_app.py` z. B. so etwas ergänzen:

```python
import os
if not os.path.exists("models/forecaster.pt"):
    import urllib.request
    os.makedirs("models", exist_ok=True)
    urllib.request.urlretrieve("https://yourserver.com/forecaster.pt", "models/forecaster.pt")
```

---

## 🖥️ GUI mit PySide6 im Docker (Linux only)

Für den Fall, dass du PySide6-GUI in Docker verwenden willst (nur unter Linux mit X11 möglich), brauchst du:

- `xhost +local:docker`
- Dockerfile mit:

```dockerfile
ENV DISPLAY=:0
```

Und startest den Container mit:

```bash
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --network=host weather-ai
```

> **Achtung:** Funktioniert nicht unter Windows/Mac ohne VNC/X11.

---

## ✅ Zusammenfassung

| Ziel | Status |
|------|--------|
| Dockerfile für Web-App | ✅ Fertig |
| Lokales Streaming über Port 8501 | ✅ |
| Automatisches Modell-Laden möglich | ✅ |
| GUI via Docker (X11) | 🟡 Optional (Linux only) |

