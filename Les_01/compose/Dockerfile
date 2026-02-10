# Gebruik een officiële Python runtime als parent image
FROM python:3.8-slim

# Stel de werkdirectory in in de container
WORKDIR /app

# Kopieer de huidige directory inhoud naar /app in de container
COPY . /app

# Installeer de vereisten
RUN pip install --no-cache-dir -r requirements.txt

# Maak poort 5000 beschikbaar voor de wereld buiten deze container
EXPOSE 5000

# Definieer de command om de app te draaien
CMD ["python", "app.py"]
