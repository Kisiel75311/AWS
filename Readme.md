# Dokumentacja Projektu: Gra Tic-Tac-Toe

## Wstęp

Projekt Tic-Tac-Toe to aplikacja webowa umożliwiająca grę w kółko i krzyżyk. Składa się z front-endu napisanego w Vue.js oraz back-endu w Pythonie z użyciem Flask. Aplikacja wykorzystuje Docker Compose do zarządzania kontenerami oraz Playwright do testowania end-to-end (E2E).

## Architektura

Projekt składa się z trzech głównych części:

- **Backend (`flaskapp-node`)**: Usługa backendowa w Pythonie/Flask, zapewniająca logikę gry i API RESTowe.
- **Frontend (`vueapp-node`)**: Interfejs użytkownika zbudowany przy użyciu Vue.js, komunikujący się z backendem.
- **Testy E2E (`playwright-e2e`)**: Automatyczne testy przeglądarkowe z użyciem Playwright.

## Funkcjonalności


## Backend (Flask)


## Frontend (Vue.js)


## Testowanie

- Testy API z wykorzystaniem pytest.
- Testy E2E z wykorzystaniem Playwright, automatyzujące działania użytkownika w przeglądarce.

## Uruchomienie Projektu

Aby uruchomić projekt, wymagane jest zainstalowanie Docker i Docker Compose. Następnie można użyć polecenia `docker-compose up` do uruchomienia wszystkich usług.

## Dostępne Endpoints API



## Struktura Projektu


## Docker Compose

Konfiguracja Docker Compose obejmuje trzy usługi: `flaskapp-node`, `vueapp-node` oraz `playwright-e2e`.





