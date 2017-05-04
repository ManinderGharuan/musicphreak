from urllib.parse import urlparse, urljoin
from scrapers.RootScraper import RootScraper
from .Items import Song


class DjjohalScraper(RootScraper):
    """
    Creates scraper which scraps djjohal.com
    """
    def __init__(self):
        super().__init__()
        self.whitelist = ['mr-johal.com']
        self.rescrapables = [
            'http://djjohal.com/',
            'https://mr-johal.com/updates.PP'
        ]
        self.done_rescrapables = False
        self.base_url = 'http://djjohal.com'

    def extract_item(self, soup):
        """
        Returns Song Item form the soup if it is an item page.
        None otherwise
        """
        pass

    def extract_next_links(self, soup, base_url):
        """
        Returns links to scrap next from the soup
        """
        pass

    def soup_has_item(self, soup):
        """
        Returns True if soup has item, False otherwise
        """
        print(soup.select('a/'))
        return
        for a in soup.find_all('a'):
            print(a)
            if (
                    a.attrs['href'].endswith('.mp3')
                    and soup.select_one('.albumCover')
                    and soup.select_one('.albumCover').find('img')
            ):
                return True

        return False

    def parse(self):
        """
        Returns list of `Song's` and assign them to `self.songs`
        """
        links = self.rescrapables

        while links:
            if self.done_rescrapables:
                links = self.get_next_links()
            else:
                self.done_rescrapables = True

            for link in links:
                link = 'https://mr-johal.com/single/57421/a-kay-tait-goriye.html'
                next_links = []
                song = None

                try:
                    soup = self.make_soup(link)
                except Exception:
                    continue

                if self.soup_has_item(soup):
                    return
                    song = self.extract_item(soup)
                    self.songs.append(song)

                return
                next_links = self.extract_next_links(soup, link)

                self.scrap_in_future(list(next_links))
                self.on_success(link)

                yield song

            return self.songs
