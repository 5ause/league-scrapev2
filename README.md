# league-scrapev2

# Report

The data analysis notebook can be found [here](Riot_01202022.ipynb)

**THE REPORT** can be found [here](writeup/Riot%20Games%20Writeup.pdf)

# Basic

The python portion of this project(in the [src](src) folder) is a web scraper that measures over 200 variables for matches of the popular game,
League of Legends. It gathers data directly from the Riot Games API, as well as from web-scraping the popular
stats website, LeagueOfGraphs.com.

Data that was collected can be found in the [data](data) folder.

I created a classification model with ~82% test accuracy, which can be found in the [writeups](writeup) folder

# Notes

I am currently in second year university. For some reason, I keep coming back to predicting League of Legends outcomes, using my newfound knowledge. Around 1 year ago, I built a data collector that only takes data from the riot games api. I used a single decision tree to create a model in R that gave me ~60% accuracy on low ranking games.

This year, I used a random forest in python, added web scraping and did more exploratory data analysis before making the model.

# Check out the code!

These can all be found in the [src](src) folder.

[main.py](src/main.py) contains the code for running the scraper. It delegates tasks to other classes.
It also contains some procedures for dealing with N/A values, and handling exceptions.

[APICollector](src/APICollector.py), [WebScrapeCollector](src/WebScrapeCollector.py) help collect
data from the API and from the web, respectively

[RequestSender](src/RequestSender.py) contains tools for sending dynamic requests.

[MainObservation](src/MainObservation.py) puts together the APICollector and WebScrapeCollector information
and produces a formatted dictionary of data, which is flattened in main.py.

# Some links that I found useful

[how to improve my model](https://www.analyticsvidhya.com/blog/2015/12/improve-machine-learning-results/)

[random forest fine tuning](https://www.analyticsvidhya.com/blog/2015/06/tuning-random-forest-model/)

[ensemble methods](https://www.analyticsvidhya.com/blog/2015/08/introduction-ensemble-learning/)

