# proxy_checker
Project for getting checked proxies.

## GENERAL USAGE
The main part of this program is `daemon.py` that perfoms scrapping and then checking of proxies from https://free-proxy-list.net/. Just keep this script running as long as you need. It will start new loop of scrapping-checking-saving **every 15 minutes.**

You can also use `scrapper.py` or `checker.py` separetly if you need it.

To recieve the list of proxies you can use **CLI** `proxy.py`.

## INSTALATION
1. **Clone** this repository.

2. Create virtual environment and **install dependencies**.
```
pip install -r requirements.txt
```

3. Create empty **PostgreSQL DB** for the proxies. You can use PgAdmin for this purpose. 

4. **Create a `.env` file** in your project and write db variables into it.

Congrats! You are ready to go!

## CLI
By default CLI will return you 10 last checked alive proxies. Open the terminal in the appropriate folder and run:
```
python proxy.py
```
There are some flags that are available for usage:
- -h - will show you all the available options
- -c [country_code] - filter results by country
- -r - returns the most reliable proxies (with highest availability rate)
- -s - returns the fastest proxies (with lowest ping)
- -n [int] - number of returning proxies
- -f [filename] - name of the file for saving proxies

_Pay attention that you cannot use -r and -s together._
