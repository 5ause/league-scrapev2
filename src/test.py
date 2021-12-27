import requests

import RequestSender
import time
import APICollector
import CustomExceptions
import Logger


def enter_api_keys():
    RequestSender.add_keys(["RGAPI-8da6ea21-bc38-4f30-9eaf-0411a6c4140a"])


def test_requests():
    enter_api_keys()

    codes = dict()

    def add_code(code, cdodes):
        if code not in cdodes:
            cdodes[code] = 1
        else:
            cdodes[code] += 1

    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/PlatypusOfCanada?api_key=<API_KEY>"

    start_time = int(time.time())
    count = 0
    while int(time.time()) < (start_time + 120):
        count += 1
        resp = RequestSender.send_request(url)
        add_code(resp.status_code, codes)
        print("count=" + str(count), ", code=" + str(resp.status_code))

    print("sent " + str(count) + " requests in " + str(int(time.time()) - start_time) + " seconds.")
    print(codes)


def test_process_url():
    assert RequestSender.process_url("www.google.ca/<A>/<B><C>", {"A": "hello", "B": "MY", "C": "man"}) == \
           "www.google.ca/hello/MYman"


def test_summoner_v4(name):
    Logger.VERBOSITY_LEVEL = "ALL"
    try:
        player = APICollector.BasicSummonerInfo(name)
        print(player.info)
        ranked_info = APICollector.SummonerRankedInfo(player)
        print(ranked_info["rank"], ranked_info["tier"], ranked_info["lp"])
        matches = APICollector.SummonerGameBuffer(player)
        match = matches.matches[0]
        game = APICollector.LeagueGame(match, player)
        print("time: " + str(game.game_time))
        print("winning team:", game.winning_team)
        print("team kills:", game.team_kills)
        print("individual data:", game.individual_data)
    except CustomExceptions.APICallException as e:
        print(e)


enter_api_keys()
# test_summoner_v4("PlatypusOfCanada")
test_summoner_v4("waste it on me")

# enter_api_keys()
# for i in range(0, 3):
#     response = RequestSender.send_request(
#         "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/PlatypusOfCanada?api_key=<API_KEY>")
#     print(response.json())
    # TODO IT TURNS OUT YOU NEED 1 API KEY FOR EACH INDIVIDUAL SUMMONER BRUHHH
    # for get_api_key maybe do request a specific key or something and let it auto sleep for u like overload the method
    # to get_api_key(key) or something
