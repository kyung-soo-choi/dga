from apscheduler.schedulers.background import BackgroundScheduler
from .utils import fetch_and_process_weather_data

scheduler = None


def start():
    """
    Startet den BackgroundScheduler, um Wetterdaten regelmäßig abzurufen und zu verarbeiten.
    Die Funktion erstellt einen Scheduler, falls dieser noch nicht existiert, und plant einen Job,
    der alle 180 Minuten die Funktion fetch_and_process_weather_data ausführt.
    """
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(fetch_and_process_weather_data, 'interval', minutes=180)
        scheduler.start()
