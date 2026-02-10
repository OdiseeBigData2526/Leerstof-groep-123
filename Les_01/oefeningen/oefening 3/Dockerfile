# Gebruik een officiële Python runtime als parent image
FROM python:3.8-slim

# Stel de werkdirectory in in de container
WORKDIR /app

# Kopieer het huidige directory inhoud naar /app in de container
COPY . /app

# Kopieer een extra bestand naar de container
COPY data.txt /app/data.txt

# Voer het Python script uit
CMD ["python", "read_file.py"]
