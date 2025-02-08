import logging

from graylog import GelfTcpHandler
from src.core.settings import get_settings

settings = get_settings()

class GraylogHandler:
    def __init__(self):
        self.handler = GelfTcpHandler(
            host=settings.GRAYLOG_HOST,
            port=settings.GRAYLOG_PORT,
            debug=settings.DEBUG,
            extra_fields=True
        )
        
        self.handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

    def get_handler(self):
        return self.handler 