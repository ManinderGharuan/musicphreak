from scrapers.RootScraper import RootScraper
from Song import Song


class MrjattScraper(RootScraper):
    def __init__(self):
        start_url = 'https://mr-jatt.com/punjabisongs-top20.html'
        super().__init__(start_url)

        self.base_url = 'https://mr-jatt.com'

    def parse(self):
        links = [link.get('href')
                 for link in self.soup.find_all('a', {'class': 'touch'})
                 if 'download' in link.get('href')]

        return links
        for link in links:
            link_soup = self.make_soup(link)
            metadata_div = link_soup.find('div', {'class': 'albumCoverSmall'})
            img = metadata_div.find('img').get('src')

            name = None
            artist = None
            album = None
            matadata = link_soup.find('div', {'class': 'albumInfo'})
            matadata_rows = [[j.strip() for j in i.text.split(':')] for i in
                             matadata.find_all('p')]

            for text in matadata_rows:
                if text[0].lower() == 'title':
                    name = text[1]
                if text[0].lower() == 'artists':
                    artist = [i.strip() for i in text[1].split(',')]
                if text[0].lower() == 'album':
                    album = text[1]

            mp3_links = {}
            all_links = []
            maybe_mp3_links = link_soup.findAll('a', {'class': 'touch'})

            for i in maybe_mp3_links:
                if i.get('herf').endswith('.mp3'):
                    all_links.append(i)

            all_links = [i for i in all_links if 'Download in' in i.text]

            for mp3 in all_links:
                if '48 kbps' in mp3.text:
                    mp3_links['48'] = mp3.get('href')
                if '128 kbps' in mp3.text:
                    mp3_links['128'] = mp3.get('href')
                if '192 kbps' in mp3.text:
                    mp3_links['192'] = mp3.get('href')
                if '320 kbps' in mp3.text:
                    mp3_links['320'] = mp3.get('href')

            song = Song(name, artist, img, mp3_links)
            self.songs.append(song)

        return self.songs
