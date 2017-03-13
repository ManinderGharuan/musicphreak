from datetime import datetime, date
from scrapers.RootScraper import RootScraper
from Items import Ranking


class RadioMirchiScraper(RootScraper):
    """
    Create scraper which scrapes radiomirchi.com for top 10 songs
    """
    def __init__(self):
        start_url = 'http://www.radiomirchi.com/more/punjabi-top-10/'
        super().__init__(start_url)

        self.base_url = 'http://www.radiomirchi.com'

    def parse(self):
        """
        Returns list of `Song`s and assign them to `self.Song`
        """
        song_containers = self.soup.select('.top01')
        song_date = self.soup.find('a', {'class': 'select'}).text.split('-')[0].strip() + ' ' + str(date.today().year)

        week = datetime.strptime(song_date, '%b %d %Y')

        for song in song_containers:
            name_artist_pair = song.find('h3').text
            name_artist_pair = [i.strip() for i in name_artist_pair.split('\n')]

            rank = song.select_one('.circle').text

            song_ranking = Ranking(
                name_artist_pair[0],
                name_artist_pair[1],
                rank,
                week
            )
            self.ranking.append(song_ranking)

        return self.ranking
