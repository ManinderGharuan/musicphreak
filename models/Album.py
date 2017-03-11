class Album():
    def __init__(self, name, release_date, poster_url):
        self.name = name
        self.release_date = release_date
        self.poster_url = poster_url

    def _absorb_db_row(self, row):
        self.id = row[0]
        self.name = row[1]
        self.release_date = [2]
        self.poster_url = [3]

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
