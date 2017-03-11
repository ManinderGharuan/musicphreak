from scrapers.RootScraper import RootScraper
from Song import Song


class JattjugadScraper(RootScraper):
    """
    Creates scraper which scraps jattjugad.com for top 20 songs
    """
    def __init__(self):
        start_url = 'http://jattjugad.xyz/mu/index.php?tnz=top20songs&cat=Punjabi_SinGle_Track&t=30days'
        super().__init__(start_url)

        self.base_url = 'http://jattjugad.xyz'

    def parse(self):
        """
        Returns list of songs after assigning them to ~self.songs~
        """
        links = [
            self.base_url + a.get('href')
            for a in self.soup.find_all('a')
            if '/mu/song/' in a.get('href')
        ]

        for link in links:
            link_soup = self.make_soup(link)
            mp3_links = {}

            for tag_td in link_soup.find_all('td'):
                if 'Title:' in tag_td.get_text():
                    song_name = (tag_td.get_text().replace('Title: ', ''))

                if 'Artists:' in tag_td.get_text():
                    artist = [i.strip() for i in tag_td.get_text().replace('Artists: ', '').split(',')]

                if 'Album:' in tag_td.get_text():
                    album = tag_td.get_text().replace('Album: ', '').strip()

            for image in link_soup.find_all('img'):
                if '/mu/thumb/' in image.get('src'):
                    image_link = self.base_url + image.get('src')

            for tag_a2 in link_soup.find_all('a'):
                if "/mu/data/" in tag_a2.get('href'):
                    url = tag_a2.get('href')

                    if '48' in url:
                        mp3_links['48'] = url
                    elif '128' in url:
                        mp3_links['128'] = url
                    else:
                        mp3_links['320'] = url

            song = Song(song_name, artist, album, self.base_url, image_link, mp3_links)
            self.songs.append(song)

        return self.songs
