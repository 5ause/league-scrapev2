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

[a guy on twitter made a similar bot](https://twitter.com/kshuna/status/1471946830342762502)
- he found that a person's personal winrate on the champ that they are playing is important.
    - I think the only way to do this is to take every single game and calculate shit... we'll find the number of games played using ranked w/l rate, and then take a max of 50 games or something and then look at each individual game to see how much the person plays the specific champ, and how much they win I guess
    - We'll also record things such as average objective damage/min, damage/min, etc. maybe? and also record the number of times they play each role or something...
- he identified the top/mid/bot/jg/sup whatever and got their personal champ win rates, that sounds interesting
- So basically we'll look at a person's role, look for other games on that champ in that role, and see how they do? in terms of objectives, gold, kp, etc.?
- So the main idea is we look at each role and give in depth metrics about their past performance, and try to predict using that.

I think that's the only way to look at the game without entering the player that's playing, we will identify each player and go like blue_top, red_mid, etc. It will be good.
