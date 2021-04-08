from loguru import logger

from args import args
if not args.debug:
    logger.remove(handler_id=None)

logger.add('activity_{time}.log',
           level="INFO",
           rotation='5 MB',
           encoding='utf-8',
           compression="zip")
