# Dokumentacja Projektu: Gra Tic-Tac-Toe

## Wstęp

Projekt Tic-Tac-Toe to aplikacja webowa umożliwiająca grę w kółko i krzyżyk. Składa się z front-endu napisanego w Vue.js oraz back-endu w Pythonie z użyciem Flask. Aplikacja wykorzystuje Docker Compose do zarządzania kontenerami oraz Playwright do testowania end-to-end (E2E).

## Architektura

Projekt składa się z trzech głównych części:

- **Backend (`flaskapp-node`)**: Usługa backendowa w Pythonie/Flask, zapewniająca logikę gry i API RESTowe.
- **Frontend (`vueapp-node`)**: Interfejs użytkownika zbudowany przy użyciu Vue.js, komunikujący się z backendem.
- **Testy E2E (`playwright-e2e`)**: Automatyczne testy przeglądarkowe z użyciem Playwright.

## Funkcjonalności

- Rozpoczęcie nowej gry.
- Wykonywanie ruchów przez graczy.
- Resetowanie gry.
- Automatyczne wykrywanie zwycięzcy lub remisu.
- Rejestracja i logowanie użytkowników.
- Przeglądanie dostępnych gier i dołączanie do nich.
- Zarządzanie stanem gry i interakcją użytkownika.

## Backend (Flask)

- Endpoints API do zarządzania grą.
- Logika gry Tic-Tac-Toe.
- Obsługa bazy danych do przechowywania stanu gry.
- Autoryzacja z użyciem JWT (JSON Web Tokens).

## Frontend (Vue.js)

- Interaktywny interfejs umożliwiający grę w kółko i krzyżyk.
- Logowanie i rejestracja użytkowników.
- Komunikacja z backendem za pomocą Axios.
- Wyświetlanie i aktualizacja stanu gry w czasie rzeczywistym.

## Testowanie

- Testy API z wykorzystaniem pytest.
- Testy E2E z wykorzystaniem Playwright, automatyzujące działania użytkownika w przeglądarce.

## Uruchomienie Projektu

Aby uruchomić projekt, wymagane jest zainstalowanie Docker i Docker Compose. Następnie można użyć polecenia `docker-compose up --build` do uruchomienia wszystkich usług.

## Dostępne Endpoints API

- `GET /api/start`: Rozpoczyna nową grę.
- `POST /api/move`: Wykonuje ruch w bieżącej grze.
- `GET /api/reset`: Resetuje grę.
- `POST /auth/register`: Rejestracja nowego użytkownika.
- `POST /auth/login`: Logowanie użytkownika i generowanie tokena JWT.
- `POST /auth/logout`: Wylogowanie użytkownika (wymaga JWT).
- `GET /api/start`: Rozpoczyna nową grę (wymaga JWT).
- `POST /api/move`: Wykonuje ruch w bieżącej grze (wymaga JWT).
- `GET /api/reset`: Resetuje grę (wymaga JWT).
- `POST /api/join`: Dołącza użytkownika do istniejącej gry (wymaga JWT).
- `GET /api/all_games`: Zwraca listę wszystkich dostępnych gier.
- `GET /api/game/<game_id>`: Zwraca szczegóły gry (wymaga JWT).

## Struktura Projektu

- `backend/`: Zawiera kod źródłowy Flask.
- `frontend/`: Zawiera kod źródłowy Vue.js.
- `e2e/`: Zawiera testy E2E Playwright.
- `docker-compose.yml`: Konfiguracja Docker Compose.

## Docker Compose

Konfiguracja Docker Compose obejmuje trzy usługi: `flaskapp-node`, `vueapp-node` oraz `playwright-e2e`.




