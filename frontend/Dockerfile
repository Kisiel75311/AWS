# Użyj obrazu Node.js
FROM node:14

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik 'package.json' i zainstaluj zależności
COPY package*.json ./
RUN npm install

# Skopiuj resztę kodu do kontenera
COPY . .

# Zbuduj aplikację
RUN npm run build

# Zainstaluj serwer HTTP do obsługi statycznych plików
RUN npm install -g http-server

# Uruchom serwer HTTP do obsługi statycznych plików
CMD [ "http-server", "dist" ]
