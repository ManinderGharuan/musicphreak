import sqlite3
from os import path


def init_db(db_path):
    SCHEMA_PATH = path.join(path.dirname(__file__), 'schema.sql')
    db = sqlite3.connect(db_path)

    with open(SCHEMA_PATH, 'r') as schema_file:
        db.cursor().executescript(schema_file.read())

    db.commit()


def get_db():
    DB_PATH = path.join(path.dirname(__file__), 'musicphreak.db')
    print(DB_PATH)

    if not path.exists(DB_PATH):
        init_db(DB_PATH)

    db = sqlite3.connect(DB_PATH)

    return db
