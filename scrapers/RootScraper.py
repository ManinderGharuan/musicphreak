from bs4 import BeautifulSoup
from requests import get
import random

user_agents = [
    'Googlebot/2.1 (+http://www.google.com/bot.html)',
    'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1) ',
    'AltaVista Intranet V2.0 AVS EVAL search@freeit.com',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
]


class RootScraper():
    """
    Root class to be subclassed by other scrapers. Provide common functionality
    for all scrapers.
    """
    def __init__(self, start_url):
        self.soup = self.make_soup(start_url)
        self.songs = []
        self.ranking = []

    def make_soup(self, url):
        """
        Takes a url, and return BeautifulSoup for that Url
        """
        header = {
            'user-agent': random.choice(user_agents)
        }

        print("Downloading page: ", url)
        return BeautifulSoup(get(url, headers=header).content, 'html.parser')

    def parse(self):
        """
        Should return list of songs after assigning them to ~self.songs~.
        To be implemented by child scrapers.
        """
        raise Exception("Implement it dumbfuck")

    def __add__(self, other):
        """
        Combine two scrapers such that their songs are unique
        """
        raise Exception("Implement it dumbfuck")
