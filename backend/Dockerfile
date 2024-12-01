FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv venv \
    && ./venv/bin/pip install --no-cache-dir -r requirements.txt \
    && ./venv/bin/python -m spacy download en_core_web_lg

ENV PATH="/app/venv/bin:$PATH"

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
