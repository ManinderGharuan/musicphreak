from urllib.parse import urlparse


class Song():
    """
    Represents a single song extracted by scrapers
    """
    def __init__(self, name, artist, album, source, image_link='',
                 mp3_links={}, released_date=None):
        self.name = name
        self.artist = artist
        self.album = album
        self.source = urlparse(source).hostname
        self.image_link = image_link
        self.mp3_links = mp3_links
        self.released_date = released_date

    def __repr__(self):
        return "<name: {} artist: {}>".format(self.name, self.artist)

    def to_dict(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "source": self.source,
            "image_link": self.image_link,
            "mp3_links": self.mp3_links,
            "released_date": self.released_date
        }


class Ranking():
    def __init__(self, name, artist, ranking, week_start_date):
        self.name = name
        self.artist = artist
        self.ranking = int(ranking)
        self.week = week_start_date

    def __repr__(self):
        return "<name: {} ranking: {} week: {}>".format(self.name, self.ranking, self.week)

    def to_dict(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "ranking": self.ranking,
            "week": self.week
        }
