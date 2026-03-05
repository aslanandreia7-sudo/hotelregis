from django.apps import AppConfig

class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'  # <--- ASEGÚRATE DE QUE DIGA 'hotel' Y NO 'web'