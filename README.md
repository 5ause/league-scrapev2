# league-scrapev2

This is a web scraper that measures over 200 variables for matches of the popular game,
League of Legends.

It gathers data directly from the Riot Games API, as well as from web-scraping the popular
stats website, LeagueOfGraphs.com.

It then saves the data to a csv.

# IMPORTANT

[Data analysis/model creation](writeup/Riot_V2.ipynb)

[Brief explanation of how the scraper works](writeup/scraping.md)

[2022/01/02] I'm currently in second year University, so my only experience with data cleaning/analysis comes from my Intro to Stats course and the few Kaggle competitions that I've done. I quickly cleaned the data and fitted a basic model in the above notebook.

(This is the second time I've done this, so I'm just keeping track of my experience with each iteration. Around 1 year ago, I built a data collector that only takes data from the riot games api. I created a model in R that gave me ~60% accuracy on low elo games)

# Check out the code!

These can all be found in the [src](src) folder.

[main.py](src/main.py) contains the code for running the scraper. It delegates tasks to other classes.
It also contains some procedures for dealing with N/A values, and handling exceptions.

[APICollector](src/APICollector.py), [WebScrapeCollector](src/WebScrapeCollector.py) help collect
data from the API and from the web, respectively

[RequestSender](src/RequestSender.py) contains tools for sending dynamic requests.

[MainObservation](src/MainObservation.py) puts together the APICollector and WebScrapeCollector information
and produces a formatted dictionary of data, which is flattened in main.py.
