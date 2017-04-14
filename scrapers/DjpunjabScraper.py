from urllib.parse import urlparse, urljoin
from scrapers.RootScraper import RootScraper
from .Items import Song


class DjpunjabScraper(RootScraper):
    """
    Creates scraper which scraps djpunjab.com for top 20 songs
    """
    def __init__(self, app):
        super().__init__(app)
        self.whitelist = ['djpunjab.com']
        self.rescrapables = [
            'http://djpunjab.com',
            'http://djpunjab.com/latest_update.php',
            'http://djpunjab.com/page/top20.html?type=week',
            'http://djpunjab.com/page/top20_month.html',
            'http://djpunjab.com/latest-bollywood-top-songs.html',
            'http://djpunjab.com/page/latest.html',
            'http://djpunjab.com/punjabi_music/latest.php?&id=2'
        ]
        self.done_rescrapables = False
        self.base_url = 'http://djpunjab.com'

    def extract_item(self, soup):
        """
        Returns Song Item from the soup if it is an item page. None otherwise
        """
        metadata_div = soup.find("div", {"class": "cont-a"})

        img = metadata_div.find('img').get('src')

        metadata_rows = [
            [j.strip() for j in i.text.split(':')]
            for i in metadata_div.find_all('p')
        ]

        name = None
        artist = None

        for text in metadata_rows:
            if text[0].lower() == 'track':
                name = text[1]

            if text[0].lower() == 'artist':
                artist = [i.strip() for i in text[1].split(',')]

            album = None

        mp3_links = {}
        maybe_mp3_links = []

        for a in soup.select('p > a'):
            if a.attrs['href'].endswith('.mp3'):
                maybe_mp3_links.append(a)

        maybe_mp3_links = [
            i for i in maybe_mp3_links if 'Download In' in i.text
        ]

        for mp3_link in maybe_mp3_links:
            if '32 Kbps' in mp3_link.text:
                mp3_links['32'] = mp3_link.attrs['href']
            if '48 Kbps' in mp3_link.text:
                mp3_links['48'] = mp3_link.attrs['href']
            if '128 Kbps' in mp3_link.text:
                mp3_links['128'] = mp3_link.attrs['href']
            if '320 Kbps' in mp3_link.text:
                mp3_links['320'] = mp3_link.attrs['href']

        return Song(name, artist, album, self.base_url, img, mp3_links)

    def extract_next_links(self, soup, base_url):
        """
        Returns links to scrap next from the soup
        """
        next_links = set()

        for a in soup.select('a'):
            link = urljoin(self.base_url, a.get('href'))

            if urlparse(link).hostname in self.whitelist:
                next_links.add((link,))

        return next_links

    def soup_has_item(self, soup):
        for a in soup.select('p > a'):
                if (
                        a.attrs['href'].endswith('.mp3')
                        and soup.find("div", {"class": "cont-a"}) is not None
                ):
                    return True

        return False

    def parse(self):
        """
        Returns list of `Song`s and assign them to `self.songs`
        """
        links = self.rescrapables

        while links:
            if self.done_rescrapables:
                links = self.get_next_links()
            else:
                self.done_rescrapables = True

            for link in links:
                next_links = []
                song = None

                try:
                    soup = self.make_soup(link)
                except Exception:
                    continue

                if self.soup_has_item(soup):
                    song = self.extract_item(soup)
                    self.songs.append(song)

                next_links = self.extract_next_links(soup, link)

                self.scrap_in_future(list(next_links))

                self.on_success(link)

                yield song

        return self.songs
