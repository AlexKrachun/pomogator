import yandexwebdav

from dotenv import load_dotenv
import os

load_dotenv()
YANDEX_USERNAME = os.environ.get('YANDEX_USERNAME')
YANDEX_PASSWORD = os.environ.get('YANDEX_PASSWORD')

conf = yandexwebdav.Config({
    "user": YANDEX_USERNAME,
    "password": YANDEX_USERNAME,
    })

conf.upload(localpath='/Bot/trash/main.png', href='/')