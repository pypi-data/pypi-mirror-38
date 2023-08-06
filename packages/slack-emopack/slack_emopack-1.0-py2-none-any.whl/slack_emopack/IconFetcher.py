import requests
import json
from urlparse import urljoin


class IconFetcher(object):

    def __init__(self):
        self.session = requests.Session()
        self.url = 'https://search.icons8.com'

    def get_icons(self, term):
        icons = []
        iconlist = None

        offset = 0

        while (iconlist and len(iconlist)) or iconlist is None:
            url = urljoin(
                self.url,
                '/api/iconsets/v4/search'
            )\
                + '?term={}&amount=50&offset={}&platform=all&language=en-US'\
                .format(term, offset)

            resp = json.loads(self.session.get(url).text)
            platforms = resp.get('platforms')
            iconlist = resp.get('icons')

            for icon in iconlist:
                for platform in platforms:
                    name_common = icon.get('commonName')
                    name = platform.lower() + '-' +\
                        icon.get('name').lower().replace(' ', '-')

                    url = 'https://img.icons8.com/{}/2x/{}.png'\
                        .format(platform, name_common)

                    icons.append((name, url))

            offset += 50

        return icons
