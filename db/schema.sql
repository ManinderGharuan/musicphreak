DROP TABLE IF EXISTS song;
CREATE TABLE song (
       id INTEGER PRIMARY KEY autoincrement,
       name TEXT NOT NULL,
       album_id INTEGER NOT NULL,
       created_at DATETIME NOT NULL,
       updated_at DATETIME NOT NULL,
       FOREIGN KEY(album_id) REFERENCES album(id)
);

DROP TABLE IF EXISTS album;
CREATE TABLE album (
       id INTEGER PRIMARY KEY autoincrement,
       name TEXT NOT NULL,
       artist_id INTEGER NOT NULL,
       release_date DATE NOT NULL,
       poster_img_url TEXT,
       created_at DATETIME NOT NULL,
       updated_at DATETIME NOT NULL,
       FOREIGN KEY(artist_id) REFERENCES artist(id)
);

DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
       id INTEGER PRIMARY KEY autoincrement,
       name TEXT NOT NULL,
       created_at DATETIME NOT NULL,
       updated_at DATETIME NOT NULL
);

DROP TABLE IF EXISTS artist_albums;
CREATE TABLE artist_albums (
       album_id INTEGER NOT NULL,
       artist_id INTEGER NOT NULL,
       created_at DATETIME NOT NULL,
       updated_at DATETIME NOT NULL,
       FOREIGN KEY(artist_id) REFERENCES artist(id),
       FOREIGN KEY(album_id) REFERENCES album(id),
       PRIMARY KEY (artist_id, album_id)
);

DROP TABLE IF EXISTS mp3s;
CREATE TABLE  mp3s (
       id INTEGER PRIMARY KEY autoincrement,
       song_id INTEGER NOT NULL,
       url TEXT NOT NULL,
       source TEXT NOT NULL,
       quality INTEGER NOT NULL,
       created_at DATETIME NOT NULL,
       updated_at DATETIME NOT NULL,
       FOREIGN KEY(song_id) REFERENCES song(id)
);
