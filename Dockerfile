FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ntp \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
 CMD curl --fail http://localhost:8080/health || exit 1

CMD ["python", "bot.py"]