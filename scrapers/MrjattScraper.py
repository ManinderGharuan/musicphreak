from scrapers.RootScraper import RootScraper
from Song import Song


class MrjattScraper(RootScraper):
    """
     Creates scraper which scraps mr-jatt.com for top 20 songs
    """
    def __init__(self):
        start_url = 'https://mr-jatt.com/punjabisong-top20-singletracks.html'
        super().__init__(start_url)

        self.base_url = 'https://mr-jatt.com'

    def parse(self):
        """
        Returns list of `Song`s and assign them to `self.songs`
        """
        links = [link.get('href')
                 for link in self.soup.find_all('a', {'class': 'touch'})
                 if 'download' in link.get('href')]

        for link in links:
            link_soup = self.make_soup(link)
            metadata_div = link_soup.find('div', {'class': 'albumCoverSmall'})
            img = metadata_div.find('img').get('src')

            name = None
            artist = None
            album = None
            released_date = None
            matadata = link_soup.find('div', {'class': 'albumInfo'})
            matadata_rows = [[j.strip() for j in i.text.split(':')] for i in
                             matadata.find_all('p')]

            for text in matadata_rows:
                if text[0].lower() == 'album':
                    name = text[1]
                if text[0].lower() == 'singer':
                    artist = [i.strip() for i in text[1].split(',')]
                if text[0].lower() == 'released':
                    released_date = text[1]

                album = name

            mp3_links = {}
            all_links = []
            maybe_mp3_links = link_soup.findAll('a', {'class': 'touch'})

            for i in maybe_mp3_links:
                if i.get('href').endswith('.mp3'):
                    all_links.append(i)

            all_links = [i for i in all_links if 'Download in' in i.text]

            source = None
            for mp3 in all_links:
                source = mp3
                if '48 kbps' in mp3.text:
                    mp3_links['48'] = mp3.get('href')
                if '128 kbps' in mp3.text:
                    mp3_links['128'] = mp3.get('href')
                if '192 kbps' in mp3.text:
                    mp3_links['192'] = mp3.get('href')
                if '320 kbps' in mp3.text:
                    mp3_links['320'] = mp3.get('href')

            song = Song(name, artist, album, source, img, mp3_links,
                        released_date=released_date)
            self.songs.append(song)

        return self.songs
