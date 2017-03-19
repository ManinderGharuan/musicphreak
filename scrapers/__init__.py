from datetime import date
import os
from scrapers.DjpunjabScraper import DjpunjabScraper
from scrapers.JattjugadScraper import JattjugadScraper
from scrapers.MrjattScraper import MrjattScraper
from models.Album import Album
from models.Song import Song
from models.Artist import Artist
from models.ArtistAlbums import ArtistAlbums
from models.Mp3s import Mp3s
from models.SongRankings import SongRankings
from itertools import groupby
from web.db import *


def run_scrapers():
    """
    Returns list of songs after running scrapers.
    """
    songs = []

    try:
        jt = JattjugadScraper()

        songs += jt.parse()
    except Exception as e:
        print("JattjugadScraper failed: ", e)

    try:
        dj = DjpunjabScraper()

        songs += dj.parse()
    except Exception as e:
        print("DjpunjabScraper failed: ", e)

    try:
        mr = MrjattScraper()

        songs += mr.parse()
    except Exception as e:
        print("MrjattScraper failed: ", e)
        raise "None of the scrapers worked. Sorry bru!"

    return songs


def save_songs_to_db(songs):
    """
    Save songs in database
    """
    db = get_db()

    try:
        cursor = db.cursor()

        for song in songs:
            song_name = song['name']
            artist_names = song['artist']
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

            for name in (artist_names or ['N/A']):
                artist_id = Artist(name).insert(cursor).id
                ArtistAlbums(album_id, artist_id).insert(cursor)

            for quality in mp3_links:
                url = mp3_links.get(quality)
                Mp3s(song_id, url, source, quality).insert(cursor)

    except IOError as error:
        print("Error while inserting new song", error)
    finally:
        db.commit()
        db.close()


def save_ranking_to_db(ranking):
    """
    Save ranking in song_rankings table
    """
    db = get_db()

    try:
        cursor = db.cursor()

        for rank in ranking:
            song_name = rank['name']
            artist_name = rank['artist']
            source = rank['source']
            song_rank = rank['ranking']
            week = rank['week']

            SongRankings(song_name, artist_name, source, song_rank, week).insert(cursor)
    except IOError as error:
        print('Error while inserting new ranking ', error)
    finally:
        db.commit()
        db.close()


def normalize_data(data):
    """
    Returns list of songs after removing the duplicate items
    """
    songs = []

    for (name, duplicates) in groupby(data, lambda row: row[0]):
        artist = []
        album = None
        release_date = None
        image_link = None
        mp3_links = {}

        for row in duplicates:
            if row[1] not in artist:
                artist.append(row[1])

            album = album or row[2]
            release_date = release_date or row[3]
            image_link = image_link or row[4]

            if row[6] not in mp3_links:
                mp3_links[row[6]] = row[5]

        songs.append({
            "name": name,
            "artist": artist,
            "album": album,
            "release_date": release_date,
            "image_link": image_link,
            "mp3_links": mp3_links
        })

    return songs
