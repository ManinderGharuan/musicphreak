class Album():
    def __init__(self, name, release_date, poster_url):
        self.name = name
        self.release_date = release_date
        self.poster_url = poster_url

    def _absorb_db_row(self, row, cursor):
        release_date = row[2]

        self.id = row[0]

        if not release_date and self.release_date:
            release_date = self.release_date
            self.update_release_date(cursor)

        self.name = row[1]
        self.release_date = release_date
        self.poster_url = row[3]

    def check_duplicate(self, cursor):
        """
        Returns row from database if album with same name exists.
        """
        duplicate_row = cursor.execute(
            """
            SELECT * FROM album WHERE name = ?
            """,
            (self.name,)
        ).fetchone()

        if duplicate_row:
            self._absorb_db_row(duplicate_row, cursor)

        return duplicate_row

    def update_release_date(self, cursor):
        """
        Update database record with new release_date
        """
        try:
            cursor.execute(
                """
                UPDATE album SET release_date=? WHERE id=?
                """, (self.release_date, self.id))
        except Exception as error:
            print('Error occurred while updating Album release_date', error)
            raise error

    def insert(self, cursor):
        """
        Insert album to database. Fail if album already exists
        """
        if self.check_duplicate(cursor):
            return self

        try:
            id = cursor.execute(
                """
                INSERT INTO album (name, release_date, poster_img_url)
                VALUES (?, ?, ?);
                """,
                (self.name, self.release_date, self.poster_url)
            ).lastrowid
        except Exception as error:
            print("Error while inserting album: ", error)
            raise error

        self.id = id

        return self
