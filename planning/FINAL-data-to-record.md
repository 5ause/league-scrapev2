Mote: 420 is ranked 5x5 queues, 400 is any draft pick queues, so for lower elo that's probably better.

Summoner name, id, puuid from summoner v4(for all players in the match)

Then for each player, get the following:

INSTEAD OF P@, GO FOR RTOP, BMID, etc. BASED ON POSITION AND SHIT

### Basic

League v4/byID
- [P@_TIER]: ranked solo duo tier
- [P@_RANK]: solo duo rank
- [P@_LP]: ranked solo duo LP 
- [P@_WINS, P@_LOSSES]: ranked #wins, #losses
- [P@_V, P@_I, P@_FB, P@_HS]: veteran, inactive, freshBlood, hotStreak

### Past Matches

get games thru matchv5, filter for ranked solo.

- [P@_RAVG_TIME] avg game times
- [P@_RPOS] teamPosition across the past few games literally write TOP MID BOT etc. with spaces in between or smth
- [P@_RKDA] (recent average kda) kills, deaths, assists
- [P@_RGPM, P@_RDMG] average goldEarned, totalDamageDealtToChampions PER MINUTE
- [P@_RVIS] average visionScore
- [P@_AVGCS] average cs/min
- [P@_RSURE] # of times gameEndedInSurrender for enemy team
- [P@_RDMGOBJ] damage to objectives / minute

### Teams from matchv5
- [P@_RWR] recent winrate, using teamId and win I guess
- [P@_AVGKP] average kill participation over past whatever games
- [P@_FB] no. times the player has gotten First blood in past 8 games
- [P@_FDRAG, P@_FHER, P@_FINH] no. of time player's TEAM has gotten first drag, herald, inhib

### LeagueOfGraphs
- [P@_CWR] champion winrate
- [P@_CPLAYED] champion #played
- [P@_CCSMIN] champion cs/min
- [P@_GOLDMIN] champion gold/min
- [P@_KDA] champion kda[(k+a)/d]
- [P@_ROLEWR] role wr
- [P@_ROLEPLAYED] role #played.

# Current Games
You can check the JSON for what data you can get on a current running game.

[here](https://riot-api-libraries.readthedocs.io/en/latest/roleid.html) is how to find role id. Check the 
github repo on the second thing. Go to examples and shit, use pip to install shit.

We're gonna get role being played(assuming you must fit top mid bot sup jg), player ids and that's ALL.
