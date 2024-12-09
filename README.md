# Analiza CV z zastosowaniem uczenia maszynowego w celu optymalizacji procesów rekrutacyjnych

## Opis projektu

Projekt składa się z dwóch głównych komponentów: **web** oraz **backend**, uruchamianych za pomocą Docker Compose. Oba komponenty mają swoje Dockerfile i są zmapowane na odpowiednie porty.

## Wymagania wstępne

- Docker (<https://docs.docker.com/get-docker/>)
- Docker Compose (<https://docs.docker.com/compose/>)

## Struktura projektu

.
├── docker-compose.yml
├── web
│   └── kod aplikacji frontendowej
├── experiments
│   ├── classification
│   │   └── kod eksperymentów - klasyfikacja CV
│   └── ranking
│       └── kod eksperymentów - ranking CV
├── data
│   └── dane do treningu modeli
└── backend
    └── kod aplikacji backendowej

## Uruchomienie projektu

1. **Uruchom aplikację za pomocą Docker Compose**:
   docker compose up

2. **Dostęp do kontenerów**:
   - Web: <http://localhost:3000>
   - Backend: <http://localhost:5000>

## Zatrzymanie kontenerów

Aby zatrzymać działanie kontenerów, użyj:
   `docker compose down` lub `Ctrl-C`
