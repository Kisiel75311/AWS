#backend/Dockerfile
# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.8

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki wymagań i zainstaluj zależności
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu do kontenera
COPY backend/ .

# Ustaw zmienną środowiskową wskazującą na port, na którym uruchomiona jest usługa
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Uruchom aplikację
CMD ["flask", "run"]
