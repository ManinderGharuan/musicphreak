from bs4 import BeautifulSoup
from requests import get


class RootScraper():
    """
    Root class to be subclassed by other scrapers. Provide common functionality
    for all scrapers.
    """
    def __init__(self, start_url):
        self.soup = self.make_soup(start_url)
        self.songs = []

    def make_soup(self, url):
        """
        Takes a url, and return BeautifulSoup for that Url
        """
        return BeautifulSoup(get(url).content, 'html.parser')

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
