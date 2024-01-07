#!/bin/bash

#aktywacja venv
source backend/venv/Scripts/activate

#instalacja zależności
pip install -r backend/requirements.txt

# Uruchomienie testów i generowanie raportów
pytest --alluredir=reports

# Wynik testów jest ignorowany; raporty są wysyłane zawsze
echo "Wysyłanie raportów do Allure TestOps..."

./allurectl.exe upload \
    --endpoint https://allure-testops.sos.pus.corp \
    --token bfdb0b73-969a-4b83-a23c-4f7c35b6a5fb \
    --project-id 2 \
    --launch-name "Flask Backend Tests" \
    reports

# Sprawdzenie, czy wysyłanie się powiodło
if [ $? -eq 0 ]; then
    echo "Raporty zostały wysłane pomyślnie."
else
    echo "Wystąpił błąd podczas wysyłania raportów."
fi
