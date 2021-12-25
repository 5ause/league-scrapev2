import requests
import CustomExceptions
import RequestSender
import Logger
import json

SUMMONER_V4_URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/<SUM_NAME>?api_key=<API_KEY>"
LEAGUE_V4_URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/<ID>?api_key=<API_KEY>"
PAST_MATCHES_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/<PUUID>/ids?queue=420&start=0&count=10&api_key=<API_KEY>"


# TODO make a function that calls the riot api, returns a dict or an error
def get_rgapi_json(response: requests.Response):
    if response.status_code == 403:
        raise CustomExceptions.APICallException("No API KEY probably")
    elif not response.ok:
        raise CustomExceptions.APICallException("API Call failed: " + str(response.content))
    else:
        Logger.debug("Successfully converted to JSON")
        return response.json()


# TODO make a function that makes an object of name id puuid from the summoner v4 data

# TODO make a summoner_v4 object that processes the league_v4 stuff
class BasicSummonerInfo:
    """
    This collects data
    """

    def __init__(self, name: str):
        response, self.api_key = send_summoner_v4(name)
        self.summoner_name, self.summoner_id, self.summoner_puuid = process_summoner_v4(get_rgapi_json(response))
        Logger.debug("Got info for " + self.summoner_name)

    def __str__(self):
        return "Name: " + self.summoner_name + ", id: " + self.summoner_id + ", puuid: " + self.summoner_puuid


class SummonerRankedInfo:
    def __init__(self, bsi: BasicSummonerInfo):
        response = send_league_v4(bsi)
        self.tier, self.rank, self.lp, self.wins, self.losses, self.veteran, self.inactive, self.freshblood, \
        self.hotstreak = process_league_v4(get_rgapi_json(response))
        Logger.debug("got ranked info for " + bsi.summoner_name)


class SummonerGameInfo:
    def __init__(self, bsi: BasicSummonerInfo):
        response = get_past_matches(bsi)
        self.matches = response.json()
        Logger.debug("Got " + str(len(self.matches)) + " matches for " + bsi.summoner_name)


def get_past_matches(bsi: BasicSummonerInfo):
    variables = {"PUUID": bsi.summoner_puuid, "API_KEY": bsi.api_key}
    return RequestSender.send_request(PAST_MATCHES_URL, variables=variables)


def send_summoner_v4(name: str):
    name = name.replace(" ", "%20")
    variables = {"SUM_NAME": name, "API_KEY": RequestSender.get_api_key()}
    return RequestSender.send_request(SUMMONER_V4_URL, variables=variables), variables["API_KEY"]


def process_summoner_v4(jason):
    sum_name = jason["name"]
    sum_id = jason["id"]
    sum_puuid = jason["puuid"]
    return sum_name, sum_id, sum_puuid


def send_league_v4(bsi: BasicSummonerInfo):
    variables = {"ID": bsi.summoner_id, "API_KEY": bsi.api_key}
    return RequestSender.send_request(LEAGUE_V4_URL, variables=variables)


def process_league_v4(jason):
    for i in jason:
        if i["queueType"] == "RANKED_SOLO_5x5":
            ptier = i["tier"]
            prank = i["rank"]
            plp = i["leaguePoints"]
            pwins = i["wins"]
            plosses = i["losses"]
            pveteran = i["veteran"]
            pinative = i["inactive"]
            pfreshblood = i["freshBlood"]
            photstreak = i["hotStreak"]
            return ptier, prank, plp, pwins, plosses, pveteran, pinative, pfreshblood, photstreak
    return None, None, None, None, None, None, None, None, None