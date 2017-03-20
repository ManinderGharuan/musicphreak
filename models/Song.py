class Song():
    def __init__(self, name, album_id, poster_img_url, release_date, artist_id):
        self.name = name
        self.album_id = album_id
        self.poster_img_url = poster_img_url
        self.release_date = release_date
        self.artist_id = artist_id

    def _absorb_db_row(self, row, cursor):
        self.id = row[0]
        self.name = row[1]
        album_id = row[2]

        if not album_id and self.album_id:
            album_id = self.album_id
            self.update_changes(cursor, "album_id", self.album_id)

        self.album_id = album_id
        self.poster_img_url = row[3]
        release_date = row[4]

        if not release_date and self.release_date:
            release_date = self.release_date
            self.update_changes(cursor, "release_date", self.release_date)

        self.release_date = release_date

    def check_duplicate(self, cursor):
        """
        Returns row from database if song with same name and album_id exists.
        """
        duplicate_row = cursor.execute(
            """
           SELECT song.* FROM artist
            INNER JOIN song_artist ON song_artist.artist_id = artist.id
            INNER JOIN song ON song.id = song_artist.song_id
            WHERE song.name=? AND artist.id=?;
            """,
            (self.name, self.artist_id)
        ).fetchone()

        if duplicate_row:
            self._absorb_db_row(duplicate_row, cursor)

        return duplicate_row

    def update_changes(self, cursor, column_name, value):
        """
        Update database record with `column_name` to new `value`
        """
        try:
            cursor.execute(
                """
                UPDATE song SET {} = ? WHERE id = ?;
                """
                .format(column_name), (value, self.id)
            )
        except Exception as error:
            print('Error occurred while updating song {}'
                  .format(column_name), error)
            raise error

    def insert(self, cursor):
        """
        Insert song to database. Fail if song already exists
        """
        if self.check_duplicate(cursor):
            return self

        try:
            id = cursor.execute(
                """
                INSERT INTO song (
                   name,
                   album_id,
                   poster_img_url,
                   release_date
                )
                VALUES (?, ?, ?, ?);
                """, (
                    self.name,
                    self.album_id,
                    self.poster_img_url,
                    self.release_date
                )
            ).lastrowid
        except Exception as error:
            print("Error while inserting song: ", error)
            raise error

        self.id = id

        return self
