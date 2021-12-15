# Data to record

## Individual Player

### Basic info

Summoner > id --> leaguev4/byId

For SOLO and FLEX, get the following:
- ranked 5x5 tier and rank
- ranked 5x5 league points

FIGURE OUT HOW CHALLENGER / GM / ETC. WORKS

- ranked winrate
- veteran, inactive, freshBlood, hotStreak

### Look at past matches

get games thru matchv5, filter for ranked solo. Then get data for the past like 10 games

my idea is to simply do m1_[parameter], for every match, but idk

- find how many times the player won/lost, using "win"
- game times
- teamPosition across the past few games literally write TOP MID BOT etc. with spaces in between or smth
- kills, deaths, assists
- goldEarned, totalDamageDealtToChampions
- visionScore
- gameEndedInSurrender
- goldEarned

Teams has some interesting info as well, you can find
- number of champ/objective/whatever kills
- You can find teamId and win here as well.

### I consulted some websites

[first site](https://www.invenglobal.com/articles/8188/five-factors-that-you-should-know-to-win-league-of-legends)
- assists, especially assists/death ratio, or something like kill participation maybe(would be done in analysis, not when collecting raw)
- team objective kills in the past few rounds, maybe over time or something like that idk
- who gets first blood, first herald, dragon, etc.(can be found in "teams")
- player average vision score in past rounds(we can see if that's indicative of their vision score in future rounds maybe)
    - and then we can find average average vision score of the players on each team.
    
[second site](https://towardsdatascience.com/league-of-legends-win-conditions-db139f1ed6ca)
- good insights as to how data analysis is done.
- So at this point I think we can try to see if players are consistent, if past behavior will decently help predict future behavior.
  - we can also look at match infos to see what win conditions are important, etc.
  
- That reminds me of OP score. Like for example RATIRL or whoever may be losing games but is ACE every game or something.
So maybe we look at that. Like cs/min + damage + objectives + kda + vision etc.
  - the only thing I can think of is to just compare each of these between winning/losing teams to determine how useful it is
  - sometimes when you get more kills, your cs/min goes down, so maybe we gotta look at like gold/min
  
LOOK AT ABOVE HYPOTHESES AND RECORD THOSE