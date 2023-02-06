from typing import Generator

import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

from settings import PROXY_SOURCE_URL
from models import get_session, Proxy, db_connect, create_table
from logger import logger


class ProxyScraper:
    """This class encapsulates all the scraping logic"""
    def __init__(self):
        self.engine = db_connect()
        create_table(self.engine)
        self.Session = get_session(self.engine)
        logger.debug('Scrapper init')

    def run(self) -> None:
        """Main method to run the scraper"""
        logger.debug('Making a request')
        soup = self.get_proxies()
        for proxy in self.parse_proxies(soup):
            self.save_proxies(proxy)
        logger.info("Proxies are scrapped")

    @staticmethod
    def get_proxies() -> BeautifulSoup:
        """Making request to the proxy source and creating the BeautifulSoup object"""
        response = requests.get(PROXY_SOURCE_URL)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    @staticmethod
    def parse_proxies(soup: BeautifulSoup) -> Generator:
        """Generator scrapes every proxy details"""
        table = soup.find('section', id='list').find('tbody').find_all('tr')
        for row in table:
            data = row.find_all('td')
            proxy = Proxy(
                ip=data[0].text,
                port=data[1].text,
                country_code=data[2].text,
                country=data[3].text,
                secure=True if data[6].text == 'yes' else False
            )
            yield proxy

    def save_proxies(self, proxy: Proxy) -> None:
        """Saves new proxies to the database. Duplicates are omitted"""
        with self.Session() as session:
            try:
                session.add(proxy)
                session.commit()
                logger.info(msg=f'Proxy {proxy.ip}:{proxy.port} is saved.')
            except IntegrityError:
                logger.exception(msg=f'Duplicated proxy {proxy.ip}:{proxy.port}.', exc_info=False)
                session.rollback()


if __name__ == '__main__':
    ProxyScraper().run()
