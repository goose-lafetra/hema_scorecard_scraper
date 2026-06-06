"""
Runs a program that controls the scraper and responds to user input.
"""
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import asyncio
import re

from .public_scraper import PublicScraper, URL_REGEX
from .roses_export import write_match_data

SCORECARD_REFRESH_TIME = 0.5 # Keep this above 0.2 to be nice to HEMAScorecard
SCRAPER_TIMEOUT = 60 * 60 * 8 # 8 Hour timeout, do not lengthen

COMMAND_QUIT = "quit"
INIT_URL="https://hemascorecard.com/scoreMatch.php?e=900&t=3717&m=431475#" # The url we init our scraper with

class ScraperConsole:

    scraper = PublicScraper(INIT_URL)
    debug = False
    is_running = False
    timeout_task : asyncio.Task
    console_task : asyncio.Task
    scraper_task : asyncio.Task
    scraper_lock = asyncio.Lock()

    def __init__(self, debug):
        self.debug = debug

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        with patch_stdout():
            self.console_task = asyncio.create_task(self.scraper_loop())
        try:
            await self.command_loop()
        finally:
            self.console_task.cancel()
    
    async def command_loop(self):

        # Create Prompt.
        session = PromptSession(": ")
        last_command = ""


        # Run echo loop. Read text from stdin, and reply it back.
        while last_command != "quit":
            try:
                last_command = await session.prompt_async()

                if self.debug:
                    # Don't catch exceptions while in debug mode
                    await self.handle_command(last_command)

                else:
                    try:
                        await self.handle_command(last_command)

                    except Exception as ex:
                        print("Unhandled exception occured! Failed to excecute command.")
                        print(ex)

                print() # Makes the output a bit prettier

            except (EOFError, KeyboardInterrupt):
                return
        
    async def scraper_loop(self):
        try:
            while True:
                if self.is_running:
                    async with self.scraper_lock:
                        self.scraper.refresh_data()
                        write_match_data(self.scraper.match_data, "out/")

                await asyncio.sleep(SCORECARD_REFRESH_TIME)

        except asyncio.CancelledError:
            print("Scraper stopped.")

    async def timeout(self):
        await asyncio.sleep(SCRAPER_TIMEOUT) 

        print("Timeout limit reached!")
        self.handle_command_stop()


    async def handle_command(self, command):
        if re.fullmatch(URL_REGEX, command) != None:
            await self.handle_command_url(command)

        elif command == "help":
            self.handle_command_help()

        elif command == "next":
            await self.handle_command_next()

        elif command == "prev":
            await self.handle_command_prev()

        elif command == "start":
            self.handle_command_start()

        elif command == "stop":
            self.handle_command_stop()

        elif command == "quit":
            print("Quitting...")

        else:
             print("Command not recognised! Run command \"help\" for a list of commands.")    

    # Sets a new match url to scrape from
    async def handle_command_url(self, command: str):
        print("Updating match url...")

        async with self.scraper_lock:
            self.scraper.set_url(command)
            self.scraper.refresh_data()
            write_match_data(self.scraper.match_data, "out/")

        print("New match data successfully retreived! (" \
              + self.scraper.match_data.left_fighter.name + " vs. " \
              + self.scraper.match_data.right_fighter.name + ")")
        
    async def handle_command_next(self):
        print("Updating match url...")

        async with self.scraper_lock:
            self.scraper.match_id += 1
            self.scraper.refresh_data()
            write_match_data(self.scraper.match_data, "out/")

        print("Next match data successfully retreived! (" \
              + self.scraper.match_data.left_fighter.name + " vs. " \
              + self.scraper.match_data.right_fighter.name + ")")

    async def handle_command_prev(self):
        print("Updating match url...")

        async with self.scraper_lock:
            self.scraper.match_id -= 1
            self.scraper.refresh_data()
            write_match_data(self.scraper.match_data, "out/")

        print("Previous match data successfully retreived! (" \
              + self.scraper.match_data.left_fighter.name + " vs. " \
              + self.scraper.match_data.right_fighter.name + ")")
        
    def handle_command_start(self):
        if self.is_running:
            print("Updates already running!")
            
        else:
            self.is_running = True
            print("Updates started!")
            self.timeout_task = asyncio.create_task(self.timeout())
            

    def handle_command_stop(self):
        if self.is_running:
            self.is_running = False
            print("Updates stopped!")

            if self.timeout_task:
                self.timeout_task.cancel()

        else:
            print("Updates already stopped!")

    # Prints out a help message
    def handle_command_help(self):
        print("List of commands:")
        print("help - displays this list of commands")
        print("next - switch to track the next match")
        print("prev - switch to tracking the previous match")
        print("start - resumes updating files")
        print("stop - pauses updating files (switching matches will still update once)")
        print("quit - exits the program")
        print("<url> - entering a match url will update the match that the scraper is targeting")


if __name__ == '__main__':
    my_scraperconsole = ScraperConsole(debug=False)
    my_scraperconsole.run()

