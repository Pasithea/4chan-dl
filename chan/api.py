import json
from Queue import Queue
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout, Timeout, HTTPError
from logger import logger
import const

class Thread(object):
    def __init__(self, board, threadnumber):
        self._board = board
        self._threadnumber = threadnumber
        self.data = self._get_img_info()
        self._IMAGE_URL = const.IMAGE_URL.format(self.board, {}, {})
        self._THUMB_URL = const.THUMB_URL.format(self.board, {}, {})

    @property
    def board(self):
        return self._board

    @property
    def threadnumber(self):
        return self._threadnumber

    @property
    def img_num(self):
        count = 0
        if 'tim' in self.data[0]:
            count = 1
        count += self.data[0]['images']
        if count == 0:
            logger.debug('there is no image in this thread.')
            raise SystemExit
        return count

    @property
    def thread_api_url(self):
        return const.THREAD_API_URL.format(self.board, self.threadnumber)

    def _get_img_info(self):
        try:
            res = requests.get(self.thread_api_url, timeout=20, proxies=const.HTTP_PROXIES)
        except (ConnectionError, HTTPError) as e:
            logger.error('{}'.format(e))
            raise SystemExit
        except (ConnectTimeout, ReadTimeout, Timeout) as e:
            logger.error('{}'.format(e))
            raise SystemExit

        if res.status_code == 200:
            return json.loads(res.content.decode('utf-8'))['posts']

        if res.status_code == 404:
            logger.error('thread not found.')
            raise SystemExit

    def thread_info(self):
        info = dict()
        info['sub'] = self.data[0].get('sub')
        info['images'] = self.img_num
        return info

    def detail_queue(self):
        q = Queue()
        for i in range(self.data.__len__()):
            if 'tim' in self.data[i]:
                props = {}
                props['high'] = self.data[i]['h']
                props['width'] = self.data[i]['w']
                props['filename'] = str(self.data[i]['tim']) + self.data[i]['ext']
                props['url'] = self._IMAGE_URL.format(self.data[i]['tim'], self.data[i]['ext'])
                props['thumburl'] = self._THUMB_URL.format(self.data[i]['tim'], self.data[i]['ext'])
                props['size'] = self.data[i]['fsize']
                q.put(props)
        return q