class Artist():
    def __init__(self, name):
        self.name = name

    def _absorb_db_row(self, row):
        self.id = row[0]
        self.name = row[1]

    def check_duplicate(self, cursor):
        """
        Returns row from database if album with same name exists.
        """
        if len(self.name) > 1:
            self.name = '{}, {}' .format(self.name[0], self.name[1])
        else:
            self.name = '{}' .format(self.name[0])

        duplicate_row = cursor.execute(
            """
            SELECT * FROM artist WHERE name = ?
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
                INSERT INTO artist (name)
                VALUES (?);
                """,
                (self.name,)
            ).lastrowid
        except Exception as error:
            print("Error while inserting artist: ", error)
            raise error

        self.id = id

        return self
