DROP TABLE IF EXISTS song;
CREATE TABLE song (
       id INTEGER PRIMARY KEY autoincrement,
       name TEXT NOT NULL,
       album_id INTEGER NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(album_id) REFERENCES album(id),
       UNIQUE (name, album_id)
);

DROP TABLE IF EXISTS album;
CREATE TABLE album (
       id INTEGER PRIMARY KEY autoincrement,
       name TEXT,
       release_date DATE,
       poster_img_url TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
       id INTEGER PRIMARY KEY autoincrement,
       name TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS artist_albums;
CREATE TABLE artist_albums (
       album_id INTEGER NOT NULL,
       artist_id INTEGER NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(artist_id) REFERENCES artist(id),
       FOREIGN KEY(album_id) REFERENCES album(id),
       PRIMARY KEY (artist_id, album_id)
);

DROP TABLE IF EXISTS mp3s;
CREATE TABLE  mp3s (
       id INTEGER PRIMARY KEY autoincrement,
       song_id INTEGER NOT NULL,
       url TEXT UNIQUE NOT NULL,
       source TEXT NOT NULL,
       quality INTEGER NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(song_id) REFERENCES song(id)
);

DROP TABLE IF EXISTS song_rankings;
CREATE TABLE song_rankings (
       id INTEGER PRIMARY KEY autoincrement,
       song_id INTEGER NOT NULL,
       artist_id INTEGER NOT NULL,
       source TEXT NOT NULL,
       rank INTEGER NOT NULL,
       week DATE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(song_id) REFERENCES song(id),
       FOREIGN KEY(artist_id) REFERENCES artist(id)
);
