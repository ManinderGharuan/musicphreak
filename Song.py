class Song():
    def __init__(self, name, artist, image_link='', mp3_links={}):
        self.name = name
        self.artist = artist
        self.image_link = image_link
        self.mp3_links = mp3_links

    def __repr__(self):
        return "<name: {} artist: {}>".format(self.name, self.artist)
