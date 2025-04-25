# Resume analysis using nachine learning to optimize recruitment processes

## Project Description

The project consists of two applications: **web** and **backend**, both run using Docker Compose.

## Prerequisites

- Docker (<https://docs.docker.com/get-docker/>)
- Docker Compose (<https://docs.docker.com/compose/>)

## Project Structure

```text
.
├── docker-compose.yml
├── web
│   └── frontend application code
├── experiments
│   ├── classification
│   │   └── experiment code – CV classification
│   └── ranking
│       └── experiment code – CV ranking
├── data
│   └── data for model training
└── backend
    └── backend application code
```

## Running the Project

```bash
docker compose up
```

## Accessing the Applications

- Web: <http://localhost:3000>  
- Backend: <http://localhost:5000>

## Stopping the Applications

```bash
Ctrl-C
```

## Removing the Applications

```bash
docker compose down
```
