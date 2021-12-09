# Planning

Checking out the API and figuring what data can be gotten. API can be found [here](https://developer.riotgames.com/apis)

## Adding API key to request
Either add X-Riot-Token= token to your headers, or ?api_key= to your URL

## Other resources
- Game constants(eg. queue types) [here](https://developer.riotgames.com/docs/lol#general_game-constants)

### summoner-v4
Information about a summoner.

Fields:
- id, puuid, accountId, name
- summonerLevel

### match-v5
Info about a user's matches. Need puuid

- /lol/match/v5/matches/by-puuid/{puuid}/ids gets back the ids of your last few matches by queue type.
 - note that 420 is ranked solo duo queueID

### Specific match
/lol/match/v5/matches/{matchId} gets info about a specific match.
- metadata, info.

Metadata
- participants: list of puuids of the participants

Info
 - participants: list of participant stuffs
   - assists
   - bountyLevel
   - championName
   - damageDealtToBuildings, damageDealtToObjectives, damageDealtToTurrets, damageSelfMitigated
   - deaths
   - gameEndedInEarlySurrender, gameEndedInSurrender
   - teamPosition > individualPosition --> best guess as to which position the player played, RGAPI suggests to use teamPosition
   - inhibitorTakedowns, inhibitorsLost
   - kills
   - puuid
   - role...? no idea what this means
   - summonerLevel
   - timeCCingOthers
   - timePlayed
   - totalDamageDealtToChampions, totalDamageTaken
   - totalTimeSpentDead
   - teamId

- teams: team infos
  - teamId
  - win
  - objectives(maybe look into this some more)

### Ranked info
/lol/league/v4/entries/by-summoner/{encryptedSummonerId} uses id from summonerv4

- queueType is important
- tier + rank is important
- leaguePoints is important if we're looking at Master+
- wins/losses could be important
- veteran = hardstuck 
- hotstreak = 3+ wins in a row
- freshBlood: probably if you're new to a division

## Some ideas of what we want to record[IMPORTANT]
Ideas that aren't basic for what to record

- Do teams have all roles filled? Eg. we'll categorize players based on their past games, then see if each team has a top, mid, bot, jg, sup play
- Does this player take objectives a lot?
- Is this player able to close out games?(aka how long/short are his past games)

Other ideas about the thing
- We could get match info after the fact and form some sort of a score, and build models that try to predict the score based on pre-game start information.
- Then we could use gradient descent or something like that, rather than a decision tree or whatever it's called.
  - Making a lot of different real-valued functions for this, and collecting data for challenger elo and lower elo games would lead to a lot of different combinations of shits



## Todos
- need to find what info you can get when a person enters a game
