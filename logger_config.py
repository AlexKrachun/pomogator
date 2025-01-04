import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                RotatingFileHandler(
                    "bot_log.log",
                    maxBytes=5 * 1024 * 1024,  # 5 МБ
                    backupCount=5,
                    encoding='utf-8'
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )

# Вызываем функцию при импорте модуля
setup_logging()