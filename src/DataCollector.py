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