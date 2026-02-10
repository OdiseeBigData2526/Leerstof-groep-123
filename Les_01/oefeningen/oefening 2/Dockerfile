# Gebruik een officiële Python runtime als parent image
FROM python:3.8-slim

# Stel de werkdirectory in in de container
WORKDIR /app

# Kopieer het huidige directory inhoud naar /app in de container
COPY . /app

# Installeer de vereisten
RUN pip install requests

# Voer het Python script uit
CMD ["python", "script.py"]
