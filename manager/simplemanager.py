import urllib

class SimpleManager:
    def __init__(self, username, password):
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/61.0.3163.100 Safari/537.36'
        self.cookie = ''
        self.username = username
        self.password = password

    def make_cookie(self, headers):
        self.cookie = ''
        for k, v in headers:
            if k.lower() == 'set-cookie':
                self.cookie += v + '; '

        self.cookie = self.cookie.rstrip(' ;')
        if not self.cookie:
            raise ValueError

    @classmethod
    def send_request(cls, url, headers, data, encoding='utf-8'):
        data = urllib.parse.urlencode(data, encoding=encoding).encode('ascii')

        request = urllib.request.Request(url)
        for k, v in headers.items():
            request.add_header(k, v)

        response = urllib.request.urlopen(request, data)
        return response

    def login(self, encoding='utf-8'):
        pass

    def check_attend(self, encoding='utf-8'):
        pass
