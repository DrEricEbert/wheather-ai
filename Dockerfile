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