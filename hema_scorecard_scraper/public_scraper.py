"""
Gathers data from HEMAScorecard and stores it in a MatchData class.
"""
import re

import requests
from .match_data import MatchData

URL_REGEX = "^https:\\/\\/hemascorecard\\.com\\/scoreMatch\\.php\\?e=([0-9]+)&t=([0-9]+)&m=([0-9]+)#?$"

class URLError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PublicScraper:
    
    match_data = MatchData()

    # Match idenifiers
    event_id = 0
    tournament_id = 0
    match_id = 0

    def __init__(self, match_url: str):
        self.set_url(match_url)
        self.refresh_data()

    def refresh_data(self):
        response = requests.get(self.get_url())

        response.raise_for_status()
        self.match_data.parse_data(response.text)

    def set_url(self, match_url: str):
        match = re.search(URL_REGEX, match_url)

        if match == None:
            raise URLError("Provided match url is not valid!")
        
        else:
            # Test that the url is valid
            response = requests.get(match_url)
            response.raise_for_status()

            self.event_id = int(match.group(1))
            self.tournament_id = int(match.group(2))
            self.match_id = int(match.group(3))

    def get_url(self):
        return "https://hemascorecard.com/scoreMatch.php?" \
                + "e=" + str(self.event_id)\
                + "&t=" + str(self.tournament_id)\
                + "&m=" + str(self.match_id) 
                







    
