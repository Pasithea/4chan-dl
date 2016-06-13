import os
import sys
import threading
import Queue
import requests
from requests.exceptions import ConnectTimeout, ConnectionError, Timeout, ReadTimeout, HTTPError
from logger import logger
import const

class Downloader(object):
    def __init__(self, path='./', threads=1, timeout=20, is_thumb=False, retry=3):
        self.path = path
        if os.path.isdir(self.path) and os.path.exists(self.path):
            pass
        else:
            os.makedirs(self.path)
        self.timeout = timeout
        self.is_thumb = is_thumb
        self.retry = retry
        self.thread_pool = []
        self.threads = threads

    def _fetch(self, q):
        while q.qsize():
            try:
                image = q.get_nowait()
                q.task_done()
            except Queue.Empty as e:
                logger.error(e)
            absp = os.path.abspath(os.path.join(os.path.realpath(self.path) +os.sep + image['filename']))
            if os.path.exists(absp):
                logger.debug('{} exists.'.format(image['filename']))
                continue
            if self.is_thumb:
                url = image['thumburl']
            else:
                url = image['url']

            retry = self.retry
            while retry:
                try:
                    res = requests.get(url, stream=True, timeout=self.timeout, proxies=const.HTTP_PROXIES)
                    if res.status_code == 200:
                        length = int(res.headers['Content-Length'])
                        logger.info('{} -- {}M now fetching.'.format(image['filename'],
                                    round(image['size']/1024.0/1024.0, 2)))
                        progress = 0.0
                        with open(absp, 'wb') as fs:
                            for chunk in res.iter_content(2048):
                                progress += len(chunk)
                                fs.write(chunk)
                                percent = round(progress / length * 100, 2)
                                sys.stdout.write('\r{} -- {}%'.format(image['filename'], percent))
                                sys.stdout.flush()
                        logger.info('{} fetched.'.format(image['filename']))
                        break
                except (ConnectionError, HTTPError) as e:
                    logger.error('connect error,retry.')
                    retry -= 1
                except (ConnectTimeout, Timeout, ReadTimeout) as e:
                    logger.error('timeout,retry')
                    retry -= 1

    def fetch(self, q):
        for i in range(self.threads):
            self.thread_pool.append(threading.Thread(target=self._fetch, args=(q, ), name='T{}'.format(i)))
        for t in self.thread_pool:
            t.start()
        for t in self.thread_pool:
            t.join()