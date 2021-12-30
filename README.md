# league-scrapev2

This is a web scraper that measures over 200 variables for matches of the popular game,
League of Legends.

It gathers data directly from the Riot Games API, as well as from web-scraping the popular
stats website, LeagueOfGraphs.com.

It then saves the data to a csv.

## Files

These can all be found in the [src](src) folder.

[main.py](src/main.py) contains the code for running the scraper. It delegates tasks to other classes.
It also contains some procedures for dealing with N/A values, and handling exceptions.

[APICollector](src/APICollector.py), [WebScrapeCollector](src/WebScrapeCollector.py) help collect
data from the API and from the web, respectively

[RequestSender](src/RequestSender.py) contains tools for sending dynamic requests.

[MainObservation](src/MainObservation.py) puts together the APICollector and WebScrapeCollector information
and produces a formatted dictionary of data, which is flattened in main.py.