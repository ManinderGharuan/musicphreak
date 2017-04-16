class Song():
    def __init__(self, name, lyrics, album_id, poster_img_url, release_date):
        self.name = name
        self.lyrics = lyrics
        self.album_id = album_id
        self.poster_img_url = poster_img_url
        self.release_date = release_date

    def _absorb_db_row(self, row, cursor):
        self.id = row[0]
        self.name = row[1]
        lyrics = row[2]
        album_id = row[3]
        poster_img_url = row[4]
        release_date = row[5]

        if not lyrics and self.lyrics:
            lyrics = self.lyrics
            self.update_changes(cursor, "lyrics", self.lyrics)

        if not album_id and self.album_id:
            album_id = self.album_id
            self.update_changes(cursor, "album_id", self.album_id)

        if not poster_img_url and self.poster_img_url:
            poster_img_url = self.poster_img_url
            self.update_changes(cursor, 'poster_img_url', self.poster_img_url)

        if not release_date and self.release_date:
            release_date = self.release_date
            self.update_changes(cursor, "release_date", self.release_date)

        self.lyrics = lyrics
        self.album_id = album_id
        self.poster_img_url = poster_img_url
        self.release_date = release_date

    def check_duplicate(self, cursor):
        """
        Returns row from database if song with same name and album_id exists.
        """
        duplicate_row = cursor.execute(
            """
            SELECT * FROM song WHERE name = ?;
            """,
            (self.name,)
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
                   lyrics,
                   album_id,
                   poster_img_url,
                   release_date
                )
                VALUES (?, ?, ?, ?, ?);
                """, (
                    self.name,
                    self.lyrics,
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
