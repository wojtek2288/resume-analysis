# Analiza CV z zastosowaniem uczenia maszynowego w celu optymalizacji procesów rekrutacyjnych

## Opis projektu

Projekt składa się z dwóch aplikacji: **web** oraz **backend**, uruchamianych za pomocą Docker Compose.

## Wymagania wstępne

- Docker (<https://docs.docker.com/get-docker/>)
- Docker Compose (<https://docs.docker.com/compose/>)

## Struktura projektu

```text
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
```

## Uruchomienie projektu

   ```bash
   docker compose up
   ```

## Dostęp do aplikacji

- Web: <http://localhost:3000>
- Backend: <http://localhost:5000>

## Zatrzymanie aplikacji

```bash
Ctrl-C
```

## Usunięcie aplikacji

```bash
docker compose down
```
