from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from webbrowser import open_new

APP_ID = "6095932"


def get_code():
    authorization_request = _construct_authorization_request()
    open_new(authorization_request)


def _construct_authorization_request():
    params = [
        ("client_id", APP_ID),
        ("display", "page"),
        ("v", "5.64"),
        ("redirect_uri", "https://api.vk.com/blank.html"),
        ("response_type", "code"),
        ("scope", "friends")
    ]
    return 'https://oauth.vk.com/authorize?' + urlencode(params)


def get_token(code):
        params = [
            ("client_id", APP_ID),
            ("client_secret", "xBjVtvZOkBCsTSZsi58w"),
            ("redirect_uri", "https://api.vk.com/blank.html"),
            ("code", code)
        ]
        url = 'https://oauth.vk.com/access_token?' + urlencode(params)
        response = urlopen(url).read()
        return loads(response.decode())['access_token']
