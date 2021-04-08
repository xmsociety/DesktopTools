import sys
from loguru import logger

from args import args
if not args.debug:
    logger.remove(handler_id=None)

# logger.add('activity_{time}.log',
#            level="INFO",
#            rotation='5 MB',
#            encoding='utf-8',
#            compression="zip")
recoder_fmt = "{time:HH:mm:ss.SSS} | {level} - {message}"
# logger.add(sys.stdout, level="DEBUG")
logger.add('./activity_logs/activity_{time:YYYY-MM-DD}.log',
           format=recoder_fmt,
           level="INFO",
           rotation='00:00',
           encoding='utf-8',
           compression="zip")
