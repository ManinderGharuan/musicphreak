from urllib.parse import urlparse
from scrapers.RootScraper import RootScraper
from .Items import Song


class DjpunjabScraper(RootScraper):
    """
    Creates scraper which scraps djpunjab.com for top 20 songs
    """
    def __init__(self, app):
        super().__init__(app)
        self.whitelist = ['djpunjab.com']
        self.rescrapables = ['http://djpunjab.com']
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

    def extract_next_links(self, soup):
        """
        Returns links to scrap next from the soup
        """
        next_links = []
        page_path = None

        for a in soup.select('a'):
            link = a.get('href')

            if (
                    link is None
                    or '#' in link
                    or link == self.base_url
                    or link == self.base_url + '/'
                    or '&type=' in urlparse(link).query
                    or 'player=' in urlparse(link).query
                    or '/facebook_image' in urlparse(link).path
                    or 'all_images' in urlparse(link).path
                    or 'index.php' in urlparse(link).path
                    or 'recommended.html' in urlparse(link).path
                    or '/policy' in urlparse(link).path
                    or '/search' in urlparse(link).path
            ):
                continue

            if not page_path:
                if len(urlparse(link).path.split('/')) > 1:
                    page_path = (urlparse(link).path.split('/'))[1]

            if './' in urlparse(link).path:
                next_links.append(self.base_url + '/' +
                                  page_path + link.replace('./', '/'))
            elif urlparse(link).hostname is None:
                next_links.append(self.base_url + link)
            elif urlparse(link).hostname in self.whitelist:
                next_links.append(link)

        return next_links

    def parse(self):
        """
        Returns list of `Song`s and assign them to `self.songs`
        """
        links = self.rescrapables

        if self.done_rescrapables:
            links = self.get_next_links()
        else:
            self.done_rescrapables = True

        if not links:
            return self.songs

        for link in links:
            maybe_item_link = False
            next_links = None

            soup = self.make_soup(link)

            if not soup:
                continue

            for a in soup.select('p > a'):
                if (
                        a.attrs['href'].endswith('.mp3')
                        and soup.find("div", {"class": "cont-a"}) is not None
                ):
                    maybe_item_link = True

            if maybe_item_link:
                song = self.extract_item(soup)
                self.songs.append(song.to_dict())

                yield song
            else:
                next_links = self.extract_next_links(soup)

                for link in next_links:
                    self.scrap_in_future(link)

            self.on_success(link)
            yield
