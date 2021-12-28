import requests
import CustomExceptions
import RequestSender
import Logger

MATCHES_COUNT = 10
QUEUE_TYPE = "420"
SUMMONER_V4_URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/<SUM_NAME>?api_key=<API_KEY>"
LEAGUE_V4_URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/<ID>?api_key=<API_KEY>"
PAST_MATCHES_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/<PUUID>/ids?queue=" + QUEUE_TYPE + "&start=0&count=<COUNT>&api_key=<API_KEY> "
MATCH_V5_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/<MATCHID>?api_key=<API_KEY>"


def get_rgapi_json(response: requests.Response):
    if response.status_code == 403:
        raise CustomExceptions.APICallException("No API KEY probably", "a")
    elif not response.ok:
        raise CustomExceptions.APICallException("API Call failed: " + str(response.content), "a")
    else:
        return response.json()


class BasicSummonerInfo:
    """
    This collects data
    """

    def __init__(self, name: str):
        self.summoner_name = name
        self.info = dict()
        for key in RequestSender.DICT_OF_KEYS:
            response = send_summoner_v4(name, key)
            data = get_rgapi_json(response)
            self.info[key] = process_summoner_v4(data)

    def get_id(self, key: str):
        return self.info[key]["id"]

    def get_puuid(self, key: str):
        return self.info[key]["puuid"]

    def __str__(self):
        return "Name: " + self.summoner_name


class SummonerRankedInfo:
    def __init__(self, bsi: BasicSummonerInfo):
        response = send_league_v4(bsi)
        self.info = process_league_v4(get_rgapi_json(response))
        Logger.debug("got ranked info for " + bsi.summoner_name)

    def is_full(self):
        return len(self.info.keys()) == 9

    def __getitem__(self, item):
        return self.info[item]

    def __contains__(self, item):
        return item in self.info


class SummonerGameBuffer:
    def __init__(self, bsi: BasicSummonerInfo):
        self.bsi = bsi
        response = get_past_matches(bsi)
        self.matches = response.json()
        Logger.debug("Got " + str(len(self.matches)) + " matches for " + bsi.summoner_name)
        if len(self.matches) < MATCHES_COUNT:
            Logger.warning("Only found " + str(len(self.matches)) + " games", sender=bsi.summoner_name)


class HistoryLeagueGame:
    def __init__(self, matchid: str, bsi: BasicSummonerInfo):
        response, self.api_key = get_game_data(matchid)
        response_json = get_rgapi_json(response)
        search_id = bsi.get_id(self.api_key)
        individual_DTO = get_individual_DTO(search_id, response_json)

        # assign basic stuff
        self.game_time = response_json["info"]["gameDuration"]

        # position, kda, goldEarned, damage to champions, vision score, cs, dmg to obj,
        self.individual_data = get_individual_player_data(individual_DTO)
        # did game end in surrender for a team, who won, team kills
        self.winning_team = get_winning_team(response_json)
        self.team_kills = get_team_kills(response_json)
        self.champions_played = get_team_champions(response_json)
        self.champion_dict = get_team_champion_names(response_json)
        Logger.debug("Got match " + matchid + " using key " + self.api_key)


class AnalysisLeagueGame:
    def __init__(self, matchid: str):
        response, self.api_key = get_game_data(matchid)
        response_json = get_rgapi_json(response)
        # Get sumname: role
        self.positions = get_team_names_and_positions(response_json)
        # Get which team won
        self.winning_team = get_winning_team(response_json)
        # Get team kills, objective info
        self.team_kills = get_team_kills(response_json)


# IMPORTANT
def get_team_names_and_positions(all_json):
    # teamid: {role: name}
    ret_dict_100 = dict()
    ret_dict_200 = dict()
    participants_info = all_json["info"]["participants"]
    for player in participants_info:
        if player["teamId"] == 100:
            ret_dict_100[player["teamPosition"]] = player["summonerName"]
        else:
            ret_dict_200[player["teamPosition"]] = player["summonerName"]
    return {"100": ret_dict_100, "200": ret_dict_200}


# unused rn
def get_team_champions(all_json):
    ret_dict = {"100": [], "200": []}
    participants_info = all_json["info"]["participants"]
    for player in participants_info:
        ret_dict[str(player["teamId"])].append(player["championId"])
    return ret_dict


# unused rn
def get_team_champion_names(all_json):
    ret_dict = dict()
    participants_info = all_json["info"]["participants"]
    for player in participants_info:
        ret_dict[player["championId"]] = player["championName"]
    return ret_dict


def get_game_data(matchid: str):
    key = RequestSender.get_api_key()
    variables = {"MATCHID": matchid, "API_KEY": key}
    return RequestSender.send_request(MATCH_V5_URL, variables=variables), key


def get_individual_player_data(player_json):
    return {"role": player_json["teamPosition"],
            "kills": player_json["kills"],
            "deaths": player_json["deaths"],
            "assists": player_json["assists"],
            "goldEarned": player_json["goldEarned"],
            "damageToChampions": player_json["totalDamageDealtToChampions"],
            "visionScore": player_json["visionScore"],
            "creeps": int(player_json["neutralMinionsKilled"]) + int(player_json["totalMinionsKilled"]),
            "damageToObjectives": player_json["damageDealtToObjectives"],
            "championName": player_json["championName"]
            }


def get_winning_team(all_json):
    for team in all_json["info"]["teams"]:
        if team["win"]:
            return team["teamId"]


def get_team_kills(all_json):
    ret_dict = dict()
    for team in all_json["info"]["teams"]:
        ret_dict[team["teamId"]] = team["objectives"]["champion"]["kills"]
    return ret_dict


def get_individual_DTO(ide: str, full_json):
    for player_data in full_json["info"]["participants"]:
        if player_data["summonerId"] == ide:
            return player_data
    raise CustomExceptions.PlayerNotFoundException("Player with id could not be found", "a")


def get_past_matches(bsi: BasicSummonerInfo):
    key = RequestSender.get_api_key()
    puuid = bsi.get_puuid(key)
    variables = {"PUUID": puuid, "API_KEY": key, "COUNT": str(MATCHES_COUNT)}
    return RequestSender.send_request(PAST_MATCHES_URL, variables=variables)


def send_summoner_v4(name: str, api_key: str):
    name = name.replace(" ", "%20")
    variables = {"SUM_NAME": name, "API_KEY": api_key}
    return RequestSender.send_request(SUMMONER_V4_URL, variables=variables)


def process_summoner_v4(jason):
    sum_id = jason["id"]
    sum_puuid = jason["puuid"]
    return {"id": sum_id, "puuid": sum_puuid}


def send_league_v4(bsi: BasicSummonerInfo):
    key = RequestSender.get_api_key()
    sid = bsi.get_id(key)
    variables = {"ID": sid, "API_KEY": key}
    return RequestSender.send_request(LEAGUE_V4_URL, variables=variables)


def process_league_v4(jason):
    ret_dict = dict()
    for i in jason:
        if i["queueType"] == "RANKED_SOLO_5x5":
            ret_dict["tier"] = i["tier"]
            ret_dict["rank"] = i["rank"]
            ret_dict["lp"] = i["leaguePoints"]
            ret_dict["wins"] = i["wins"]
            ret_dict["losses"] = i["losses"]
            ret_dict["veteran"] = i["veteran"]
            ret_dict["inactive"] = i["inactive"]
            ret_dict["freshblood"] = i["freshBlood"]
            ret_dict["hotstreak"] = i["hotStreak"]
    return ret_dict
