from scrapers.RootScraper import RootScraper
from Song import Song


class DjpunjabScraper(RootScraper):
    def __init__(self):
        start_url = 'http://djpunjab.com/page/top20.html?type=week'
        super().__init__(start_url)

        self.base_url = 'http://djpunjab.com'

    def parse(self):
        links = [
            self.base_url + link.attrs['href']
            for link in self.soup.find('ol').find_all('a')
        ]

        for link in links:
            link_soup = self.make_soup(link)
            metadata_div = link_soup.find("div", {"class": "cont-a"})
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

            mp3_links = {}
            maybe_mp3_links = []

            for a in link_soup.select('p > a'):
                if a.attrs['href'].endswith('.mp3'):
                    maybe_mp3_links.append(a)

            maybe_mp3_links = [i for i in maybe_mp3_links if 'Download In' in i.text]

            for mp3_link in maybe_mp3_links:
                if '32 Kbps' in mp3_link.text:
                    mp3_links['32'] = mp3_link.attrs['href']
                if '48 Kbps' in mp3_link.text:
                    mp3_links['48'] = mp3_link.attrs['href']
                if '128 Kbps' in mp3_link.text:
                    mp3_links['128'] = mp3_link.attrs['href']
                if '320 Kbps' in mp3_link.text:
                    mp3_links['320'] = mp3_link.attrs['href']

            song = Song(name, artist, img, mp3_links)
            self.songs.append(song)

        return self.songs
