from .attendmanager import AttendManager
import urllib
import ssl


class TorenzoaManager(AttendManager):
    def __init__(self, username, password, login_url, attend_url, comment):
        super().__init__(username=username, password=password, login_url=login_url,
                         attend_url=attend_url, comment=comment)

    def login(self, encoding='utf-8'):
        try:
            headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded',
                       'Upgrade-Insecure-Requests': 1}
            data = {'r': 'home', 'a': 'login', 'id': self.username, 'pw': self.password, 'x': '0', 'y': '0'}
            context = ssl._create_unverified_context()

            response = self.send_request(url=self.login_url, headers=headers, data=data, context=context
                                         , encoding=encoding)
            self.make_cookie(response.info().items())
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as e:
            print(e)
            return False
        else:
            return True

    def check_attend(self, encoding='utf-8'):
        try:
            r = 'home'
            c = '120'
            m = 'attend1'
            a = 'atdck'
            atd_text = self.comment

            # check attendadnce
            headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded',
                       'Cookie': self.cookie}
            data = {'r': r, 'c': c, 'm': m, 'a': a, 'atd_text': atd_text}
            context = ssl._create_unverified_context()

            response = self.send_request(url=self.attend_url, headers=headers, data=data, context=context
                                         , encoding=encoding)
            content = response.read().decode(encoding)

            if content.find('발도장') < 0:
                return False

        except (urllib.error.URLError, urllib.error.HTTPError, IndexError, ValueError):
            return False
        else:
            return True
