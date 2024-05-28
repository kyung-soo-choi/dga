# Verwenden Sie ein Python-Slim-Image, um die Bildgröße zu reduzieren.
FROM python:3.10-slim

# Legen Sie das Arbeitsverzeichnis fest.
WORKDIR /app

# Kopieren Sie zuerst nur die Abhängigkeitsdateien, um die Verwendung des Caches zu optimieren.
COPY requirements.txt .

# Aktualisieren Sie pip und installieren Sie die Anforderungen.
# Verwenden Sie die Option `--no-cache-dir`, um den pip-Cache zu deaktivieren.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopieren Sie die restlichen Dateien.
COPY . .

# Starten Sie den Server. `python manage.py runserver` ist für die Entwicklung gedacht, daher sollten Sie für die Produktion gunicorn oder ähnliches in Betracht ziehen.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]