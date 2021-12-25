# TODO make a function that calls the riot api, returns a dict or an error

# TODO make a function that makes an object of name id puuid from the summoner v4 data

# TODO make a summoner_v4 object that processes the league_v4 stuff

class SampleClass:
    def __init__(self, summoner_name):
        json = self.send_request(summoner_name)
        self.process_json(json)

    def process_json(self, json):
        self.summoner_name = ""

    def send_request(self, summoner_name):
        pass


class DataCollector:
    """
    This collects data
    """
    def __init__(self):
        self.summoner_name = None
        self.summoner_id = None
        self.summoner_puuid = None

    def process_summoner_v4(self, json):
        self.summoner_name = json["name"]
        self.summoner_id = json["id"]
        self.summoner_puuid = json["puuid"]

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