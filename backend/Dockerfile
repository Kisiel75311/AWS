# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.8

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik wymagań i zainstaluj zależności
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu do kontenera
COPY . .

# Ustaw zmienną środowiskową wskazującą na port, na którym uruchomiona jest usługa
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV FLASK_ENV=development

RUN #pytest --alluredir=reports

# Uruchom aplikację
CMD ["flask", "run", "--debug"]
