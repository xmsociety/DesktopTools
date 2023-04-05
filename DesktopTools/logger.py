import sys

from loguru import logger

from .args import args

if not args.debug:
    logger.remove(handler_id=None)

# logger.add('activity_{time}.log',
#            level="INFO",
#            rotation='5 MB',
#            encoding='utf-8',
#            compression="zip")
recoder_fmt = "{time:HH:mm:ss.SSS} | {level} - {message}"
# logger.add(sys.stdout, level="DEBUG")
logger.add(
    "./activity_logs/activity_{time:YYYY-MM-DD}.log",
    format=recoder_fmt,
    level="INFO",
    rotation="00:00",
    encoding="utf-8",
    compression="zip",
)

slog_prefix = "Hlhyw - "
logger.add(
    "./activity_logs/server_{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="00:00",
    encoding="utf-8",
    filter=lambda x: slog_prefix in x["message"],
    compression="zip",
)


class CustomLog:
    def __init__(self, prefix):
        self.prefix = prefix

    def debug(self, msg):
        logger.debug(f"{self.prefix}{msg}")

    def info(self, msg):
        logger.info(f"{self.prefix}{msg}")

    def warning(self, msg):
        logger.warning(f"{self.prefix}{msg}")

    def error(self, msg):
        logger.error(f"{self.prefix}{msg}")


slogger = CustomLog(slog_prefix)
