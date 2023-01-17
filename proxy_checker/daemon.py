import time
from multiprocessing import Process

from scrapper import ProxyScraper
from checker import ProxyChecker


def run():
    while True:
        start = time.time()
        ProxyScraper().run()
        ProxyChecker().run()
        t = 900 - (time.time() - start)
        print(f'Will sleep for {t} seconds.')
        time.sleep(t)


if __name__ == '__main__':
    daemon = Process(target=run, daemon=True)
    daemon.start()
    daemon.join()
