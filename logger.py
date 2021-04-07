from loguru import logger

logger.add('activity_{time}.log',
           level="INFO",
           rotation='5 MB',
           encoding='utf-8',
           compression="zip")
