from .simplemanager import SimpleManager
import urllib
from lxml import html
import datetime
import random


class TwoCPUManager(SimpleManager):
    def __init__(self, username, password, login_url, check_url, attend_url):
        SimpleManager.__init__(self, username=username, password=password)
        self.login_url = login_url
        self.check_url = check_url
        self.attend_url = attend_url

    def login(self, encoding='utf-8'):
        headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'url': 'http://www.2cpu.co.kr', 'mb_id': self.username, 'mb_password': self.password}

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

            s_date = datetime.date.today().isoformat()
            current_id = ''
            at_type = str(random.randrange(1, 4))
            at_memo = '사은품은 내꺼!'

            # check attendadnce
            headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded',
                       'Cookie': self.cookie}
            data = {'s_date': s_date, 'currentId': current_id, 'at_type': at_type, 'at_memo': at_memo}
            response = self.send_request(url=self.attend_url, headers=headers, data=data, encoding=encoding)
            content = response.read().decode(encoding)

            if content.find('포인트 획득') < 0:
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
