import logging
from settings import CONSOLE_LOGGER_LEVEL, FILE_LOGGER_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('proxy_check.log')
c_handler.setLevel(CONSOLE_LOGGER_LEVEL)
f_handler.setLevel(FILE_LOGGER_LEVEL)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)
