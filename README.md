# HEMA Scorecard Scraper

A simple web scraping program to get data from HEMA Scorecard to text files for OBS to consume. Created for IFG's Tournament of the Roses 2026. It is not affiliated with HEMA Scorecard in any way. Made without the use of any AI tools.

### Legal Notice

By using this software you agree to only use the web scraper during events and test runs of events. There exist several safeguards to try and prevent you from spamming HEMA Scorecard with http requests, but if you modify the software, that may occur. For that reason, any modifications to this software must not poll the site more the 5 times per secound and must retain the original timeout of 8 hours or less.

Don't make me take this package offline.

*This work is licensed under* <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">

## Installation

_This guide is for unix based systems, commands for Windows installation may vary._

1. Ensure you have Python 3 installed.

2. Run `python3 -m pip -install hema_scorecard_scraper` though a terminal.

## Usage

Once HEMA Scorecard Scraper has been installed, you can start the program from the terminal using the command `python3 -m hema_scorecard_scraper.scraper_console`.

While the scraper is running, you should have a console in the terminal that you can type commands into. Note that the scraper console is in the "stopped" position by default and you will need to run the `start` command to start fetching data. Files will be outputted into a directory named `out` located wherever you are running the program from.



## Commands

### help

Displays this list of commands.

### next

Switches the scraper to track the next match by match number. Normally this will advance to the next match in the pool, but if you are at the end of a pool, it will advance to the next pool. Also writes the data to the files immidently.

### prev

Same as the `next` command except it increments the match number down, not up.

### start

Starts running the scraper in the background. Updates every half second. The scraper is initially in the stopped position so you will have to run this command once to get things going once you have it pointed at the right match. If the program is still running 8 hours after you've started this command, it will time out run the `stop` command. This is meant to prevent someone from leaving this program running in the background by accident.

### stop

Stops the scraper running in the background.

### quit

Exits the program entirely.

### \<url\>

Sets the scraper to track a specific match. The indended use case is for you to copy the url of the match from the HEMA Scorecard site, and paste it into the console. (You do not need to type `<url>`, just enter the url itsself.)

## Output Information

### Left/Right/Match Prefixes

All fighter data files are prependded with either `fighter_left` or `fighter_right` depending on if they appear on the left or right side of the HEMA Scorecard display. Match data files are prepended with the `match` prefix.

### Fighter Name

The name of the fighter as it appears on HEMA scorecard.

### Fighter School

The name of the fighter's school as it appears on HEMA scorecard.

### Fighter Score

The current score of the fighter.

### Match Doubles

The number of doubles present in the match.

## Why doesn't this scraper capture match time?

Because of how HEMA Scorecard is coded, match time is a little more difficult to grab. Also, for the Tournament of Roses ruleset it's not particularly important. (Matches very rarely come down to time) Because of this, the Roses streaming team didn't need match time. If it's imporant for your event, feel free to fork this repository and make a pull request when you have it working!


