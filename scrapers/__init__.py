from scrapers.DjpunjabScraper import DjpunjabScraper
from scrapers.JattjugadScraper import JattjugadScraper
from scrapers.MrjattScraper import MrjattScraper
from scrapers.RadioMirchiScraper import RadioMirchiScraper
from models.Album import Album
from models.Song import Song
from models.Artist import Artist
from models.SongArtist import SongArtist
from models.Mp3s import Mp3s
from models.SongRankings import SongRankings
from web.db import get_db


def run_scrapers(app):
    """
    Returns list of songs after running scrapers.
    """
    song_count = 0
    db = get_db(app)

    try:
        jt = JattjugadScraper(app)

        for song in jt.parse():
            if song:
                app.logger.info("Got a song {}".format(song))
                song_count += 1

                save_song_to_db(song, db)
    except Exception as e:
        print("JattjugadScraper failed: ", e)

    try:
        dj = DjpunjabScraper(app)

        for song in dj.parse():
            if song:
                app.logger.info("Got a song {}".format(song))
                song_count += 1

                save_song_to_db(song, db)
    except Exception as e:
        print("DjpunjabScraper failed: ", e)

    # try:
    #     mr = MrjattScraper(app)

    #     for song in mr.parse():
    #         if song:
    #             app.logger.info("Got a song {}".format(song))
    #             songs.append(song)
    # except Exception as e:
    #     print("MrjattScraper failed: ", e)

    db.close()

    print('******************************')
    print('**  SAVED {} SONGS TO DB  ***'.format(song_count))
    print('******************************')


def save_song_to_db(song, db):
    """
    Save song in database
    """
    try:
        cursor = db.cursor()

        song_name = song.name
        artists = song.artists
        lyrics = song.lyrics
        album_name = song.album
        source = song.source
        poster_url = song.image_link
        mp3_links = song.mp3_links
        release_date = song.released_date
        album_id = None

        if album_name is not None:
            album_id = Album(album_name).insert(cursor).id

        song_id = Song(
            song_name,
            lyrics,
            album_id,
            poster_url,
            release_date
        ).insert(cursor).id

        for artist in (artists or [{'name': None, type: None}]):
            artist_id = Artist(artist['name'], artist['type']) \
                        .insert(cursor).id
            SongArtist(song_id, artist_id).insert(cursor)

        for quality in mp3_links:
            url = mp3_links.get(quality)
            Mp3s(song_id, url, source, quality).insert(cursor)

        db.commit()
    except IOError as error:
        print("Error while inserting new song", error)


def run_ranking_scrapers(app):
    """
    Returns list of songs after running ranking scrapers.
    """
    rankings = []

    try:
        rm = RadioMirchiScraper(app)

        rankings += rm.parse()
    except Exception as e:
        print("RadioMirchiScraper failed: ", e)

    print('******************************')
    print('**  SAVING RANKINGS TO DB  ***')
    print('******************************')

    return save_rankings_to_db(rankings, app)


def save_rankings_to_db(ranking, app):
    """
    Save ranking in song_rankings table
    """
    db = get_db(app)

    try:
        cursor = db.cursor()

        for rank in ranking:
            song_name = rank.name
            artist_name = rank.artist
            source = rank.source
            song_rank = rank.ranking
            week = rank.week

            for artist in artist_name:
                SongRankings(
                    song_name,
                    artist,
                    source,
                    song_rank,
                    week
                ).insert(cursor)
    except IOError as error:
        print('Error while inserting new ranking ', error)
    finally:
        db.commit()
        db.close()
