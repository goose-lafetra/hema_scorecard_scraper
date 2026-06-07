"""
Parses and stores html data from HEMA Scorecard matches so that it can be used by the larger program.
"""

import re

class ParseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FighterData:
    label = "Blank Label" # Used in debugging only
    name = "FirstName LastName"
    school_name = "SchoolName"
    current_score = 0

    # Regex patterns for above data
    REGEX_NAME = "<span style='font-size:20px;'> (.+?)<\\/span>"
    REGEX_SCHOOL_NAME = "<span style='font-size:15px;'>\\s+(.+?)\\s+<\\/span>"
    REGEX_CURRENT_SCORE = "<span style='font-size:60px;'>\\s+([0-9/]+?)\\s+<\\/span>"

    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        return self.label + " fighter: Name: [" + self.name + "] School: [" + self.school_name + "] Score: [" + str(self.current_score) + "]"
    
    def parse_data(self, html):

        match = re.search(self.REGEX_NAME, html)
        if match == None:
            print("Could not find match for " + self.label + " fighter's name in html!")
            self.name = "???"
        else:
            self.name = match.group(1)

        match = re.search(self.REGEX_SCHOOL_NAME, html)
        if match == None:
            print("search not find match for " + self.label + " fighter's school name in html!")
            self.school_name = "???"
        else:
            self.school_name = match.group(1)

        match = re.search(self.REGEX_CURRENT_SCORE, html)
        if match == None:
            print("Could not find match for " + self.label + " fighter's current score in html!")
            self.current_score = "/" # Slash is the 
        else:
            self.current_score = match.group(1)


class MatchData:
    left_fighter = FighterData("left")
    right_fighter = FighterData("right")
    doubles_count = 0

    # Regex patterns for above data
    REGEX_FIGHTER_DATA = "<!-- Fighter information -->([\\s\\S]+?)<!-- Input Fields -->"
    REGEX_DOUBLES = "<span >[\\W\\w]*?([0-9]) Double[\\W\\w]*?<\\/span>"

    def __str__(self):
        return "Doubles: [" + str(self.doubles_count) + "] Fighters: [" + str(self.left_fighter) + " / " + str(self.right_fighter) + "]"

    def parse_data(self, html: str):

        doubles_result = re.search(self.REGEX_DOUBLES, html)
        if doubles_result == None:
            print("Could not find doubles for match! Assuming 0.")
            self.doubles_count = 0

        else:
            self.doubles_count = int(doubles_result.group(1))
        
        if len(re.findall(self.REGEX_FIGHTER_DATA, html)) != 2:
            raise ParseError("Could not find correct number of fighters in match HTML!")

        for i, match in enumerate(re.finditer(self.REGEX_FIGHTER_DATA, html)):

            if i > 1:
                raise ParseError("More than 2 fighters found in match HTML!")
            
            else:
                if i == 0:
                    self.left_fighter.parse_data(match.group(1))
                else:
                    self.right_fighter.parse_data(match.group(1))
            
        


