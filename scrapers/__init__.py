from scrapers.DjpunjabScraper import DjpunjabScraper
from scrapers.JattjugadScraper import JattjugadScraper
from scrapers.MrjattScraper import MrjattScraper
import json
from datetime import date
import os
from db import get_db
from pprint import pprint
from models.Album import Album
from models.Song import Song
from models.Artist import Artist
from models.ArtistAlbums import ArtistAlbums
from models.Mp3s import Mp3s

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__package__)), 'data')
JSON_FILENAME = '{}/{}.json' .format(DATA_DIR, date.today())


def run_scrapers():
    """
    Returns list of songs after running scrapers.

    Returns result of first scraper that finishes without error, otherwise raise an exception.
    """
    try:
        jt = JattjugadScraper()

        return jt.parse()
    except Exception as e:
        print("JattjugadScraper failed: ", e)

    try:
        dj = DjpunjabScraper()

        return dj.parse()
    except Exception as e:
        print("DjpunjabScraper failed: ", e)

    try:
        mr = MrjattScraper()

        return mr.parse()
    except Exception as e:
        print("MrjattScraper failed: ", e)
        raise "None of the scrapers worked. Sorry bru!"


def save_songs_to_db(songs):
    """
    Save songs in database
    """
    db = get_db()

    try:
        cursor = db.cursor()

        for song in songs:
            song_name = song['name']
            artist_name = song['artist']
            album_name = song['album']
            source = song['source']
            poster_url = song['image_link']
            mp3_links = song['mp3_links']
            release_date = song['released_date']

            album_id = Album(
                album_name,
                release_date,
                poster_url
            ).insert(cursor).id

            song_id = Song(song_name, album_id).insert(cursor).id
            artist_id = Artist(artist_name).insert(cursor).id
            ArtistAlbums(album_id, artist_id).insert(cursor)

            for quality in mp3_links:
                url = mp3_links.get(quality)
                Mp3s(song_id, url, source, quality).insert(cursor)
    except IOError as error:
        print("Error while inserting new song", error)
    finally:
        db.commit()
        db.close()


def get_data():
    """
    Returns data from ~run_scrapers~ and create json file with data.

    If JSON file for <today> exists, returns data from this file
    instead of re-running scrapers.
    """
    data = None

    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)

        files = os.listdir(DATA_DIR)

        for i in files:
            if os.path.join(DATA_DIR, i) != JSON_FILENAME:
                os.remove(os.path.join(DATA_DIR, i))
    except IOError:
        print("Error occurred while cleaning data dir")

    try:
        with open(JSON_FILENAME, 'r') as f:
            data = json.load(f)
    except IOError:
        data = run_scrapers()   # list of songs
        data = [song.to_dict() for song in data]  # list of dicts

        with open(JSON_FILENAME, 'w') as f:
            f.write(json.dumps(data))

    return data
