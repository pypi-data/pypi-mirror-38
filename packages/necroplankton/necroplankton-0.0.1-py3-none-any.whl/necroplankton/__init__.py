import hashlib

import requests

__author__ = 'necroplankton'


class _Hash(object):
    def __init__(self):
        pass

    @staticmethod
    def md5(source):
        md5 = hashlib.md5()
        md5.update(source.encode('utf-8'))
        return md5.hexdigest()


class Fetch(object):
    def __init__(self):
        self.hash = _Hash()
        self.output_dir = '.'

    def img(self, url, headers=None, cookies=None):
        if not headers:
            headers = {
                'pragma': 'no-cache',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en;q=1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1)' +
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'cache-control': 'no-cache',
            }
        if not cookies:
            cookies = {}
        result = requests.get(url, headers=headers, cookies=cookies)
        local_filename = self.hash.md5(url)[:5]
        after_fix = url.split('.')[-1]

        with open(f'{self.output_dir}/{local_filename}.{after_fix}', 'wb') as f:
            for chunk in result.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print(f'Fetch Success {local_filename}')


fetch = Fetch()

if __name__ == '__main__':
    fetch.img('https://cloud.rainy.me/beach.jpg')
