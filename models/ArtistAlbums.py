class ArtistAlbums():
    def __init__(self, album_id, artist_id):
        self.album_id = album_id
        self.artist_id = artist_id

    def _absorb_db_row(self, row):
        self.id = row[0]
        self.album_id = row[1]
        self.artist_id = row[2]

    def check_duplicate(self, cursor):
        """
        Returns row from database if album with same name exists.
        """
        duplicate_row = cursor.execute(
            """
            SELECT * FROM artist_albums WHERE album_id = ? AND artist_id = ?
            """,
            (self.album_id, self.artist_id)
        ).fetchone()

        if duplicate_row:
            self._absorb_db_row(duplicate_row)

        return duplicate_row

    def insert(self, cursor):
        """
        Insert album to database. Fail if album already exists
        """
        if self.check_duplicate(cursor):
            return self

        try:
            id = cursor.execute(
                """
                INSERT INTO artist_albums (album_id, artist_id)
                VALUES (?, ?);
                """,
                (self.album_id, self.artist_id)
            ).lastrowid
        except Exception as error:
            print("Error while inserting artist_albums: ", error)
            raise error

        self.id = id

        return self
