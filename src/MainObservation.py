from typing import List

from APICollector import AnalysisLeagueGame, BasicSummonerInfo, SummonerGameBuffer, SummonerRankedInfo, \
    HistoryLeagueGame

import WebScrapeCollector
import CustomExceptions
import Logger


def create_player(summoner_name: str):
    try:
        Logger.debug("Attempting to get info", summoner_name)
        bsi = BasicSummonerInfo(summoner_name)
        ranked_info = SummonerRankedInfo(bsi).info
        games_to_investigate = SummonerGameBuffer(bsi)
        games = []
        for matchid in games_to_investigate.matches:
            games.append(HistoryLeagueGame(matchid, bsi))
        Logger.message("got info", summoner_name)
        return PlayerData(bsi, ranked_info, games)
    except Exception:
        raise CustomExceptions.SummonerException(summoner_name, msg="Couldn't Process Summoner", thype="a")
        print("hello")


class PlayerData:
    def __init__(self, bsi, ranked_info, games):
        self.basic = bsi
        self.ranked_info = ranked_info
        self.games = games

    def __str__(self):
        name = "name: " + self.basic.summoner_name + "\n"
        r_info = self.ranked_info.info
        ranked = "ranked: " + r_info["tier"] + " " + r_info["rank"] + " " + str(r_info["lp"]) + "\n"
        return name + ranked


class GameObservation:
    # you enter a game id
    def __init__(self, gameid: str, bad_players=[]):
        # TODO make it possible to manually create an AnalysisLeagueGame and initialize this thing.
        # it gets basic game info, like wins, team stuff and shit
        self.game = AnalysisLeagueGame.api_init(gameid)
        for player in self.game.players:
            if player in bad_players:
                raise CustomExceptions.InputException("Game " + gameid + " contained a bad player(" + player + ")")
        # teamid: {role: name}
        team_100_players = self.game.positions["100"].copy()
        team_200_players = self.game.positions["200"].copy()

        # gets data for each player in each role on each team
        # this should side effect so we're good
        for role in team_100_players:
            sum_name = team_100_players[role]
            summoner = create_player(sum_name)
            team_100_players[role] = summoner
        for role in team_200_players:
            sum_name = team_200_players[role]
            summoner = create_player(sum_name)
            team_200_players[role] = summoner

        self.players = {"100": team_100_players, "200": team_200_players}
        # so now we have "100": {role: PlayerData}
        Logger.message("GOT ONE OBSERVATION", gameid)


# THE GOAL IS TO FILL IN MISSING VALUES WITH NONE AND STUFF

# Make sure ranked stats are populated, then you can access pd.ranked_info for it
def check_ranked_stats(pd: PlayerData):
    for key in ["tier", "rank", "lp", "wins", "losses", "veteran", "inactive", "freshblood", "hotstreak"]:
        if key in pd.ranked_info:
            continue
        else:
            pd.ranked_info.info[key] = None
            Logger.warning("Missing ranked " + key + " for player " + pd.basic.summoner_name)


# Gets a LOT of game stats for a player.
def get_game_stats(pd: PlayerData):
    pd.games: List[HistoryLeagueGame]

    positions = []
    total_kda = 0
    total_gold = 0
    total_damage_to_champs = 0
    total_vision_score = 0
    total_creeps = 0
    total_dmg_to_obj = 0
    total_time = 0
    total_wins = 0
    total_games = 0
    total_kp = 0
    for game in pd.games:
        try:
            fill_hlg_na(game)
        except CustomExceptions.InputException:
            continue
        indiv_data = game.individual_data
        # position
        total_time += game.game_time
        # TODO older versions give milliseconds, if this is >1000 then divide by 1000 basically...
        positions.append(indiv_data["role"])
        total_kda += (indiv_data["kills"] + indiv_data["assists"]) / max(1, indiv_data["deaths"])
        total_kp += (indiv_data["kills"] + indiv_data["assists"]) / max(1, game.team_kills[indiv_data["team"]])
        total_gold += indiv_data["goldEarned"]
        total_damage_to_champs += indiv_data["damageToChampions"]
        total_vision_score += indiv_data["visionScore"]
        total_creeps += indiv_data["creeps"]
        total_dmg_to_obj += indiv_data["damageToObjectives"]
        total_games += 1
        if game.winning_team == indiv_data["team"]:
            total_wins += 1

    total_minutes = total_time / 60
    position_str = ""
    for position in positions:
        position_str += position + " "
    ret_dict = {"avg_game_time": total_minutes / total_games,
                "positions_played": position_str.strip(),
                "avg_kda": total_kda / total_games,
                "avg_kp": total_kp / total_games,
                "avg_vision": total_vision_score / total_games,
                "avg_cs": total_creeps / total_minutes,
                "goldpm": total_gold / total_minutes,
                "dmgpm": total_damage_to_champs / total_minutes,
                "dmg_to_obj_pm": total_dmg_to_obj / total_minutes,
                "wr": total_wins / total_games}
    return ret_dict


# Helper
def fill_hlg_na(hlg: HistoryLeagueGame):
    for key in ["role", "kills", "deaths", "assists", "goldEarned", "damageToChampions", "visionScore", "creeps",
                "damageToObjectives", "championName"]:
        if key not in hlg.individual_data:
            hlg.individual_data[key] = 0

    if "team" not in hlg.individual_data:
        raise CustomExceptions.InputException("Found no winning team in a game", "a")


# GET CHAMP STATS
def get_champ_stats(sum_name, champ_name):
    games_played = None
    winrate = None
    soup = WebScrapeCollector.get_response(sum_name, WebScrapeCollector.LOG_URL_CHAMPIONS)
    champ_play_wr = WebScrapeCollector.get_champ_wr_played(soup, champ_name)
    # {'gamesPlayed': '172', 'winrate': '0.72093023255814', 'champion': 'Lee Sin'} or None
    if champ_play_wr is not None and "gamesPlayed" in champ_play_wr and "winrate" in champ_play_wr:
        games_played = champ_play_wr["gamesPlayed"]
        winrate = champ_play_wr["winrate"]
    else:
        Logger.warning("Couldn't find champ info for " + sum_name + "(" + champ_name + ")")
    return {"champ_games_played": games_played, "champ_winrate": winrate}


# GET ROLE STATS
def get_role_stats(sum_name, role_name):
    # role wr time
    # ["Jungler", "Top", "AD Carry", "Mid", "Support"]
    role_dict = {"JUNGLE": "Jungler", "TOP": "Top", "BOTTOM": "AD Carry", "MIDDLE": "Mid", "UTILITY": "Support"}
    soup = WebScrapeCollector.get_response(sum_name, WebScrapeCollector.LOG_URL_1)

    # {"role": role, "played": wr_dict[role][1], "winrate": wr_dict[role][2]}
    response_dict = WebScrapeCollector.find_role_wr(soup, role_dict[role_name])
    played = None
    winrate = None
    if response_dict is not None and "played" in response_dict and "winrate" in response_dict:
        played = response_dict["played"]
        winrate = response_dict["winrate"]
    else:
        Logger.warning("Couldn't find role info for " + sum_name)
    return {"role_total_played": played, "role_wr": winrate}


# I want {teamId: {roleId: allData}}
def get_alllll_stats(go: GameObservation):
    teams = {"100": None, "200": None, "winning_team": go.game.winning_team}
    players_processed = 0
    for team in ["100", "200"]:
        role_dict = dict()
        for role in go.players[team]:
            player = go.players[team][role]  # this is a PlayerData object
            check_ranked_stats(player)
            Logger.verbose("Checked ranked stats for a player")

            name = player.basic.summoner_name
            position = role
            champ = go.game.champs[name]

            game_stats = get_game_stats(player)
            ranked_stats = player.ranked_info
            Logger.verbose("Processed API stats for a player")

            role_stats = get_role_stats(name, position)
            champ_stats = get_champ_stats(name, champ)
            Logger.verbose("Processed League of Graph stats for a player")

            role_dict[role] = {"game_stats": game_stats,
                               "ranked_stats": ranked_stats,
                               "role_stats": role_stats,
                               "champ_stats": champ_stats}
            players_processed += 1
            Logger.debug("Processed stats for " + str(players_processed) + " players", "CHECKPOINT")
        teams[team] = role_dict
        # teamid: {roleid: {game_stats, etc.}}
    return teams

# to flatten, we probably just append team id and position name to every variable.
# then we put together game_stats, ranked_stats, role_stats, champ_stats
# so we'll end up with like 100_UTILITY_lp for example
