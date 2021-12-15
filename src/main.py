import Logger
import logging

# I want to be able to get ALL the data from a match and save it to a bunch of SQL databases,
# then be able to get the appropriate shit whenever I want from the database to form a spreadsheet.

Logger.alert("something bad happened", sender="main.Log")
Logger.message("whatever")
Logger.message("hello")
Logger.warning("warning!!")

# a = Logger.ColoredLogger("Scraper")
# a.info("bruh")
# a.debug("bruh2")

# logging.basicConfig(level=logging.INFO)
# logging.info("asdfkjasdlfjsadkfas")
# logging.warning("bruh")