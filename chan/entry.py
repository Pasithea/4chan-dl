import socket
import socks
from cli import parse_argument
from api import Thread
from downloader import Downloader
from logger import logger
import const

def main():
    args = parse_argument()

    try:
        if args.socks5[0] and args.socks5[1]:
            if args.proxy:
                logger.error('invalid proxy protocol count.')
                raise SystemExit
            socks.set_default_proxy(socks.SOCKS5, args.socks5[0], int(args.socks5[1]),
                                    True, args.socks5[2], args.socks5[3])
            socket.socket = socks.socksocket
    except Exception as e:
        logger.error('invalid socks5 proxy arguments.')
        raise SystemExit

    t = Thread(args.board, args.thread)
    if not args.downloading:
        thread_info = t.thread_info()
        logger.info('/{}/ - {} - {}'.format(args.board, thread_info['sub'], const.BOARDS[args.board]))
        logger.info('total images - {}'.format(thread_info['images']))
    else:
        downloader = Downloader(path=args.path, threads=args.threads, timeout=args.timeout,
                                is_thumb=args.thumb)
        q = t.detail_queue()
        downloader.fetch(q)

if __name__ == '__main__':
    main()