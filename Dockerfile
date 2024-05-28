# Verwenden eines Python-Slim-Images, um die Bildgröße zu reduzieren.
FROM python:3.10-slim

# Festlegen des Arbeitsverzeichnisses.
WORKDIR /app

# Zuerst nur die Abhängigkeitsdateien kopieren, um die Verwendung des Caches zu optimieren.
COPY requirements.txt .

# Aktualisieren von pip und Installieren der Anforderungen.
# Die Option `--no-cache-dir` deaktiviert den pip-Cache.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopieren der restlichen Dateien.
COPY . .

# Starten des Servers.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]