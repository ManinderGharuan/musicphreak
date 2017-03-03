from scrapers.DjpunjabScraper import DjpunjabScraper
from scrapers.JattjugadScraper import JattjugadScraper
from scrapers.MrjattScraper import MrjattScraper
import json
from datetime import date
import os


DATA_DIR = './data/'
JSON_FILENAME = '{}{}.json' .format(DATA_DIR, date.today())


def run_scrapers():
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


def get_data():
    data = None

    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)

        files = os.listdir(DATA_DIR)

        for i in files:
            if DATA_DIR + i != JSON_FILENAME:
                os.remove(DATA_DIR + i)
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
