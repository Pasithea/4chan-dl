import argparse
import urlparse
from logger import logger
import const

def parse_argument():
    desc = "4chan thread images downloader."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--download', dest='downloading', action='store_true',
                        help='start downloading images of a thread.')
    parser.add_argument('--thumb', dest='thumb', action='store_true',
                        help='download thumbnails only.')
    parser.add_argument('-b', '--board', dest='board', metavar='board', action='store',
                        help='tag name of board,example:[w].')
    parser.add_argument('-t', '--thread', dest='thread', metavar='thread', action='store',
                        help='number of thread')
    parser.add_argument('-p', '--path', dest='path', metavar='path', action='store',
                        default='./', help='folder where images save as,default current folder.')
    parser.add_argument('--threads', dest='threads', metavar='threads', action='store', type=int,
                        default=5, help='multi threads download,default 5,max 10.')
    parser.add_argument('--timeout', dest='timeout', metavar='seconds', action='store',
                        default=20, help='timeout of image download,default 20s.')
    parser.add_argument('--http-proxy', dest='proxy', metavar='url', action='store',
                        help='http proxy,example:[https://127.0.0.1:9000].')
    parser.add_argument('--socks5-proxy', dest='socks5', metavar='addr port', action='store', nargs='+',
                        default=[None,None], help='socks5 proxy,example:[127.0.0.1 1080 username password].')

    args = parser.parse_args()


    if not args.board or not args.thread:
        logger.debug('board and thread are both required.')
        parser.print_help()
        raise SystemExit

    # if str(args.board) not in const.BOARDS.keys():
    #     logger.debug('invalid board tag name.')
    #     raise SystemExit

    if not args.thread.isdigit():
        logger.debug('invalid thread number.')
        raise SystemExit

    if args.threads>10 or args.threads<=0:
        logger.debug('invalid threads count.')
        raise SystemExit

    if args.proxy:
        url = urlparse.urlparse(args.proxy)
        const.HTTP_PROXIES = {url.scheme.lower():args.proxy}

    if len(args.socks5) == 2:
        args.socks5.extend([None, None])

    if len(args.socks5) == 3 or len(args.socks5) == 1:
        logger.debug('invalid socks5 proxy arguments.')
        raise SystemExit

    return args

