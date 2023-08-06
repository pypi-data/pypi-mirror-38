import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from fake_useragent import UserAgent
import threading


class Importer(object):

    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password
        self.headers = {
            'User-Agent': UserAgent().random
        }
        self.session = requests.Session()
        self.token = None
        self.status = None

    def get_crumb(self):
        resp = self.session.get(self.url, headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        return soup.find('input', {'name': 'crumb'}).get('value')

    def login(self):
        resp = self.session.post(
            self.url,
            allow_redirects=True,
            headers=self.headers,
            data={
                'signin': 1,
                'has_remember': 1,
                'crumb': self.get_crumb(),
                'email': self.email,
                'password': self.password,
                'remember': 'on'
            }
        )
        self.token = resp.text\
            .split('api_token:')[1].split('"')[1].split('"')[0]

        return resp

    def upload_emojis(self, emojis):
        added = []

        def _upload_emoji(session, token, name, image):
            resp = self.session.post(
                urljoin(self.url, '/api/emoji.add'),
                data={
                    'mode': 'data',
                    'name': name,
                    'token': self.token
                },
                files={'image': image},
                allow_redirects=False

            )

            resp.raise_for_status()

        for name, url in emojis:
            if name in added:
                continue

            t = threading.Thread(target=_upload_emoji, args=(
                self.session,
                self.token,
                name,
                self.session.get(url, stream=True).raw
            ))
            added.append(name)
            t.daemon = True
            t.start()

            if self.status:
                self.status(added, emojis)
