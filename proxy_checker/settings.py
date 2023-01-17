import os
import logging
from dotenv import load_dotenv

load_dotenv()

PROXY_SOURCE_URL = 'https://free-proxy-list.net/'
CHECK_PROXY_URL = 'https://httpbin.org/ip'

PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_USER = os.getenv('PG_USER')
PG_PSSWRD = os.getenv('PG_PSSWRD')
PG_DATABASE = os.getenv('PG_DATABASE')

RESOURCES = ['https://httpbin.org/ip',
             'https://en.wiktionary.org/wiki/Wikipedia',
             'http://www.testingmcafeesites.com/index.html',
             'https://quotes.toscrape.com/',
             ]

CONSOLE_LOGGER_LEVEL = logging.DEBUG
FILE_LOGGER_LEVEL = logging.WARNING
