from .simplemanager import SimpleManager
import urllib
from lxml import html


class ETorrentManager(SimpleManager):
    def __init__(self, username, password, login_url, check_url, attend_url):
        SimpleManager.__init__(self, username=username, password=password)
        self.login_url = login_url
        self.check_url = check_url
        self.attend_url = attend_url

    def login(self, encoding='utf-8'):
        headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'url': 'https://www.etorrent.kr', 'mb_id': self.username, 'mb_password': self.password}

        try:
            response = self.send_request(url=self.login_url, headers=headers, data=data, encoding=encoding)
            self.make_cookie(response.info().items())

        except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
            return False
        else:
            return True

    def check_attend(self, encoding='utf-8'):
        try:
            headers = {'User-Agent': self.USER_AGENT, 'Cookie': self.cookie}
            data = dict()
            response = self.send_request(url=self.check_url, headers=headers, data=data, encoding=encoding)
            content = response.read().decode(encoding)

            root = html.fromstring(content)

            at_memo = root.xpath('/html/body/table[3]/tr/td/table[1]/tr/td[3]/form/div[2]/input[1]/@value')[0]
            at_memo2 = root.xpath('/html/body/table[3]/tr/td/table[1]/tr/td[3]/form/div[2]/input[2]/@value')[0]

            # check attendadnce
            headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded',
                       'Cookie': self.cookie}
            data = {'clicks': 1, 'at_memo': at_memo, 'at_memo2': at_memo2}

            response = self.send_request(url=self.attend_url, headers=headers, data=data, encoding=encoding)
            content = response.read().decode(encoding)

            if content.find('출석체크완료') < 0:
                return False

        except (urllib.error.URLError, urllib.error.HTTPError, IndexError, ValueError):
            return False
        else:
            return True

    def attend_today(self, encoding='utf-8'):
        result = self.login(encoding=encoding)
        if not result:
            return False

        return self.check_attend(encoding=encoding)
