from django.apps import AppConfig
from django.utils.timezone import now
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from . import jobs
            jobs.start()
