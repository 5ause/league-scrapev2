from APICollector import AnalysisLeagueGame, BasicSummonerInfo, SummonerGameBuffer, SummonerRankedInfo, \
    HistoryLeagueGame

import APICollector
import Logger


def create_player(summoner_name: str):
    bsi = BasicSummonerInfo(summoner_name)
    ranked_info = SummonerRankedInfo(bsi)
    games_to_investigate = SummonerGameBuffer(bsi)
    games = []
    for matchid in games_to_investigate.matches:
        games.append(HistoryLeagueGame(matchid, bsi))
    Logger.message("got info", summoner_name)
    return PlayerData(bsi, ranked_info, games)


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


class MainObservation:
    # you enter a game id
    def __init__(self, gameid: str):
        # it gets basic game info, like wins, team stuff and shit
        self.game = AnalysisLeagueGame(gameid)
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
        Logger.message("GOT ONE OBSERVATION", gameid)


