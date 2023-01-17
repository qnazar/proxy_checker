from concurrent.futures import ThreadPoolExecutor
import datetime

import requests
from requests.exceptions import ProxyError, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError, ProxyError as PrEr, MaxRetryError

from models import get_session, Proxy, db_connect
from settings import CHECK_PROXY_URL, RESOURCES
from logger import logger


class ProxyChecker:
    """This class encapsulates all the checking logic"""
    def __init__(self):
        logger.debug('Checker init')
        self.session = get_session(db_connect())()
        self.proxy_list = self._load_proxies()
        self.direct_responses = [requests.get(RESOURCE) for RESOURCE in RESOURCES]
        logger.info(f'Made direct requests. Responses: {self.direct_responses}.')

    def run(self):
        """Main function to run the checker"""
        logger.debug('Check started')
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(self._perform_check, self.proxy_list)
        logger.debug('Check complete')
        logger.debug('Saving results')
        self.session.commit()
        self.session.close()
        logger.debug('Results are saved')

    def _perform_check(self, proxy: Proxy):
        """"""
        logger.info(f'Checking {proxy.ip}:{proxy.port}')
        is_alive = self._is_alive(proxy)
        proxy.last_checked = datetime.datetime.now()
        if is_alive:
            direct_response, proxy_response = self._get_ping(proxy)
            self._is_clean(proxy, direct_response, proxy_response)

    def _load_proxies(self):
        logger.debug('Proxies are loaded')
        return self.session.query(Proxy).all()

    def _is_alive(self, proxy: Proxy):
        proxy_str = f'{proxy.ip}:{proxy.port}'
        proxies = {'http': proxy_str, 'https': proxy_str}
        try:
            requests.get(CHECK_PROXY_URL, proxies=proxies, timeout=3)
        except (ProxyError, ConnectTimeoutError, PrEr, OSError, MaxRetryError,
                TimeoutError, ConnectionResetError, ConnectTimeout):
            logger.exception(f'Proxy {proxy.ip}:{proxy.port} is dead', exc_info=False)
            proxy.is_alive = False
        else:
            proxy.is_alive = True
            proxy.check_passed += 1
            logger.debug(f'Proxy {proxy.ip}:{proxy.port} is Alive')
        finally:
            proxy.total_checks += 1
            proxy.availability = proxy.check_passed / proxy.total_checks
            return proxy.is_alive

    def _get_ping(self, proxy: Proxy):
        pings = []
        proxy_str = f'{proxy.ip}:{proxy.port}'
        proxies = {'http': proxy_str, 'https': proxy_str}

        for url, direct_response in zip(RESOURCES, self.direct_responses):
            try:
                proxy_response = requests.get(url, proxies=proxies, timeout=5)
            except:
                logger.error(f'Unable to fetch {url} with {proxy_str}')
                continue
            else:
                direct_response_time = direct_response.elapsed
                proxy_response_time = proxy_response.elapsed
                ping = proxy_response_time - direct_response_time
                pings.append(ping)

        avg_ping = sum(pings, datetime.timedelta(0)) / len(pings)
        proxy.ping = avg_ping.total_seconds()
        return direct_response, proxy_response

    def _is_clean(self, proxy: Proxy, direct_response, proxy_response):
        proxy._is_clean = direct_response.text == proxy_response.text


if __name__ == '__main__':
    ProxyChecker().run()

