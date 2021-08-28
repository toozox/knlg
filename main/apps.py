from django.apps import AppConfig
from os import environ


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    knlg_folder = environ.get('HOME') + "/kb/knlg/"
