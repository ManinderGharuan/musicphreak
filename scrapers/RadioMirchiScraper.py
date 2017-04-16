from datetime import datetime, date
from scrapers.RootScraper import RootScraper
from .Items import Ranking


class RadioMirchiScraper(RootScraper):
    """
    Create scraper which scrapes radiomirchi.com for top 10 songs
    """
    def __init__(self, app):
        super().__init__(app)
        self.urls_to_scrap = {
            'punjabi': 'http://www.radiomirchi.com/more/punjabi-top-10/',
            'hindi': 'http://www.radiomirchi.com/more/mirchi-top-20/'
        }
        self.base_url = 'http://www.radiomirchi.com'

    def parse(self):
        """
        Returns list of `Song`s and assign them to `self.Song`
        """

        for (ranking_type, link) in self.urls_to_scrap.items():
            try:
                soup = self.make_soup(link)
            except Exception:
                continue

            song_date = soup.find(
                'a', {'class': 'select'}
            ).text.split('-')[0].strip() + ' ' + str(date.today().year)

            week = datetime.strptime(song_date, '%b %d %Y')

            song_containers = soup.select('.top01')

            for song in song_containers:
                song_name = None
                artist = []
                rank = None

                name_artist_pair = song.find('h3').text
                name_artist_pair = [
                    i.strip() for i in name_artist_pair.split('\n')
                ]
                song_name = name_artist_pair[0].strip()
                artist = [
                    i.strip() for i in name_artist_pair[1].split(',')
                ]

                rank = song.select_one('.circle').text

                song_ranking = Ranking(
                    song_name,
                    artist,
                    self.base_url,
                    rank,
                    week
                )
                self.ranking.append(song_ranking)

            return
            return self.ranking
