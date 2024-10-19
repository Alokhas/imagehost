FROM python:3.9-slim

RUN apt-get update && apt-get install -y ntp

# Your existing Dockerfile commands...
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
