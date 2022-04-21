# league-scrapev2

# Report

The data analysis notebook can be found [here](Riot_01202022.ipynb)

**THE REPORT** can be found [here](writeup/Riot%20Games%20Writeup.pdf)

# The Project

Using web scraping and the official Riot Games API, I collected useful data from thousands of games of the popular game, League of Legends. League of Legends is a game in which two teams compete to destroy each other's base. I analyzed the data and created a model to classify games as "win" or "loss" for the blue team.

The python portion of this project(in the [src](src) folder) is a web scraper that measures over 200 variables for matches of the game. It gathers data directly from the Riot Games API, as well as from web-scraping the popular
stats website, LeagueOfGraphs.com.

Data that was collected can be found in the [data](data) folder.

I created a classification model with ~82% test accuracy, which can be found in the [data analysis notebook](Riot_01202022.ipynb)

# The code

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

