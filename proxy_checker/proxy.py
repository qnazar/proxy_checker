from argparse import ArgumentParser

from models import db_connect, get_session, Proxy


parser = ArgumentParser(
    prog='proxy',
    description='CLI for getting the list of proxies. Please run ProxyCheckerDaemon to update your DB.',
    epilog='Thank you for using this service.'
)

group = parser.add_mutually_exclusive_group()

parser.add_argument('-n', '--number',
                    action='store', default=10, type=int,
                    help='Defines the number of proxies to return. Default: 10')

parser.add_argument('-f', '--file',
                    action='store', default='proxy.txt', type=str,
                    help='Path to file for saving results. Default: proxy.txt')

group.add_argument('-s', '--speed',
                   action='store_true',
                   help='The fastest proxies (the lowest ping).')

group.add_argument('-r', '--reliable',
                   action='store_true',
                   help='The most reliable proxies (the highest availability rate).')

parser.add_argument('-c', '--country',
                    action='store', type=str,
                    help='Filter by country code. Example: -c "CA" -> returns proxies from Canada.')

args = parser.parse_args()


def response(args):
    with get_session(db_connect())() as session:
        query = session.query(Proxy).filter_by(is_alive=True)
        if args.country:
            query = query.filter_by(country_code=args.country)
        if args.speed or args.reliable:
            query = query.order_by(Proxy.ping.desc() if args.speed else Proxy.availability.desc())
        query = query.order_by(Proxy.last_checked.desc()).limit(args.number)
        proxy = query.all()

    with open(args.file, 'w') as file:
        file.writelines([f'{p.ip}:{p.port}\n' for p in proxy])
    for p in proxy:
        print(p.ip, p.port)


if __name__ == '__main__':
    response(args)
