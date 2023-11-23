from django.apps import AppConfig
from django.db import connection

class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction'
    def ready(self):
        cursor = connection.cursor()
        
