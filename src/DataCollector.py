import requests
import CustomExceptions
import RequestSender
import Logger

SUMMONER_V4_URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/<SUM_NAME>?api_key=<API_KEY>"


# TODO make a function that calls the riot api, returns a dict or an error
def get_rgapi_json(response: requests.Response):
    if response.status_code == 403:
        raise CustomExceptions.APICallException("No API KEY probably")
    elif not response.ok:
        raise CustomExceptions.APICallException("API Call failed: " + str(response.content))
    else:
        return response.json()

# TODO make a function that makes an object of name id puuid from the summoner v4 data

# TODO make a summoner_v4 object that processes the league_v4 stuff


def send_summoner_v4(name: str):
    name = name.replace(" ", "")
    variables = {"SUM_NAME": name}
    return RequestSender.send_request(SUMMONER_V4_URL, variables=variables)


def process_summoner_v4(json):
    sum_name = json["name"]
    sum_id = json["id"]
    sum_puuid = json["puuid"]
    return sum_name, sum_id, sum_puuid


class BasicSummonerInfo:
    """
    This collects data
    """

    def __init__(self, name: str):
        response = send_summoner_v4(name)
        self.summoner_name, self.summoner_id, self.summoner_puuid = process_summoner_v4(get_rgapi_json(response))
        Logger.debug("Got info for " + self.summoner_name)

    def __str__(self):
        return "Name: " + self.summoner_name + ", id: " + self.summoner_id + ", puuid: " + self.summoner_puuid


"""
Examples

Given =
{
    "id": "lnLIOrFoH-2ZW3YHduv7TyeVUcJJkaIdNdSpdaIQZUBbX7U",
    "accountId": "PZMNBb6Bj01iYWjnM_bkbe4W_Db2C_RS4Pn9ciPpMGLJKfk",
    "puuid": "g0IivRIr4OJCLCB2tnuIm0F9_6W_7bb3ki5ON1-nJiIBs7Wy1uXXQ5ZDXjGIzPb3aBSiPTiAobdGfg",
    "name": "PlatypusOfCanada",
    "profileIconId": 744,
    "revisionDate": 1640142865000,
    "summonerLevel": 390
}

Take, Summoner name, id, puuid from summoner v4

Andrewli = DataCollector() 
Andrewli.process_summoner_v4(json)
"""
