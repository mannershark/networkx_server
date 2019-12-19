
import logging
from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthCheckFilter())


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return 'GET /healthcheck' not in record.getMessage()


workers = 1
timeout = 60
bind = ':8008'
errorlog = '-'
accesslog = '-'
logger_class = CustomGunicornLogger
