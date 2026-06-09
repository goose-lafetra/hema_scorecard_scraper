"""
Exports matchdata to text files for use with OBS and the Tournament of Roses livestream.
"""
import os

from .match_data import MatchData, FighterData

# Definitions for output filenames
FILENAME_MATCH_DOUBLES = "match_doubles.txt"
# Note: Fighter filenames will be prefixed by "fighter" + "_" + label + "_"
FILENAME_FIGHTER_PREFIX = "fighter"
FILENAME_FIGHTER_NAME = "name.txt"
FILENAME_FIGHTER_SCHOOLNAME = "school.txt"
FILENAME_FIGHTER_SCORE = "score.txt"

ROSES_SLASH_SCORE_DISPLAY = " "

'''
Writes a single data file.
'''
def write_data_file(path: str, filename: str, data: str):
    if not os.path.exists(path):
        os.makedirs(path)

    # Sometimes useful for debuging
    #print("Writing to " + filename)

    with open(path + filename, "w", encoding="utf-8") as file:
        file.write(data)

def write_fighter_data(fighter: FighterData, path=""):
    file_prefix = FILENAME_FIGHTER_PREFIX + "_" + fighter.label + "_"

    write_data_file(path, file_prefix + FILENAME_FIGHTER_NAME, fighter.name)
    write_data_file(path, file_prefix + FILENAME_FIGHTER_SCHOOLNAME, fighter.school_name)

    if fighter.current_score == "/":
        write_data_file(path, file_prefix + FILENAME_FIGHTER_SCORE, ROSES_SLASH_SCORE_DISPLAY)
    else:
        write_data_file(path, file_prefix + FILENAME_FIGHTER_SCORE, str(fighter.current_score))



def write_match_data(match: MatchData, path=""):

    # Write general match data
    write_data_file(path, FILENAME_MATCH_DOUBLES, str(match.doubles_count))

    # Write fighter data
    write_fighter_data(match.left_fighter, path)
    write_fighter_data(match.right_fighter, path)


