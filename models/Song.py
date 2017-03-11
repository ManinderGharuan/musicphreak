class Song():
    def __init__(self, name, album_id):
        self.name = name
        self.album_id = album_id

    def _absorb_db_row(self, row):
        self.id = row[0]
        self.name = row[1]
        self.album_id = [2]

    def check_duplicate(self, cursor):
        """
        Returns row from database if album with same name exists.
        """
        duplicate_row = cursor.execute(
            """
            SELECT * FROM song WHERE name = ?
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
                INSERT INTO song (name, album_id)
                VALUES (?, ?);
                """,
                (self.name, self.album_id)
            ).lastrowid
        except Exception as error:
            print("Error while inserting song: ", error)
            raise error

        self.id = id

        return self
