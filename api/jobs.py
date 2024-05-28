from apscheduler.schedulers.background import BackgroundScheduler
from .utils import fetch_and_process_weather_data

scheduler = None


def start():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(fetch_and_process_weather_data, 'interval', minutes=180)
        scheduler.start()
