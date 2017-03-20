from models.Artist import Artist
from models.Song import Song
from models.SongArtist import SongArtist


class SongRankings():
    def __init__(self, song, artist, source, rank, week):
        self.song = song
        self.artist = artist
        self.source = source
        self.rank = rank
        self.week = week

    def _absorb_db_row(self, row, cursor):
        self.song_id = row[1]
        self.artist_id = row[2]
        self.source = row[3]
        self.rank = row[4]
        self.week = row[5]

    def check_duplicate(self, cursor):
        """
        Returns row from database if song_rankings with same week exists
        """
        duplicate_row = cursor.execute(
            """
            SELECT * from song_rankings WHERE rank = ? AND week = ?;
            """,
            (self.rank, self.week)
        ).fetchone()

        if duplicate_row:
            self._absorb_db_row(duplicate_row, cursor)

        return duplicate_row

    def get_song_artist_id(self, cursor):
        """
        Select song_id and artist_id from database
        """
        try:
            song_artist_id = cursor.execute(
                """
                SELECT song.id AS "song_id", artist.id AS "artist_id"
                FROM song_artist
                INNER JOIN song ON song_artist.song_id = song.id
                INNER JOIN artist ON song_artist.artist_id = artist.id
                WHERE song.name=? and artist.name=?;
                """,
                (self.song, self.artist)
            ).fetchone()

            return song_artist_id
        except Exception as error:
            print("Error while selecting song_id and artist_id: ", error)
            raise error

    def insert(self, cursor):
        """
        Insert song_rankings to database. Fail if song rankings_already exits
        """
        song_artist_id = self.get_song_artist_id(cursor)

        if not song_artist_id:
            artist_id = Artist(self.artist).insert(cursor).id
            song_id = Song(self.song,
                           None,
                           None,
                           None,
                           artist_id).insert(cursor).id
            SongArtist(song_id,
                       artist_id).insert(cursor)
        else:
            song_id = song_artist_id[0]
            artist_id = song_artist_id[1]

        if self.check_duplicate(cursor):
            return self

        try:
            id = cursor.execute(
                """
                INSERT INTO song_rankings
                (song_id, artist_id, source, rank, week)
                VALUES
                (?, ?, ?, ?, ?);
                """,
                (song_id,
                 artist_id,
                 self.source,
                 self.rank,
                 self.week)
            ).lastrowid
        except Exception as error:
            print("Error while inserting song_rankings: ", error)
            raise error

        self.id = id

        return self
