# NOLAgnarwhal Fantasy Football Repository
Hello and thanks for stopping by! This repo is where I store scripts, data and visualizations pertaining to Fantasy Football. Below you'll find the run-down on what things I've got up and running. Feel free to clone, fork, pull and contribute in any way!
___

## Up-and-Running Projects
___

### [Opponent Implied Ceiling](https://github.com/NOLAgnarwhal/fantasy-football/tree/master/opponent_implied_ceiling)
___
Opponent Implied Ceiling (OIC) creates a points projection dataframe for fantasy players based on their upcoming matchups by scraping individual stats from FantasyPros and team stats from FootballDB. Average individual performance in fantasy point metrics are scraped and then compared with average overall team offense in the same categories to create a percentage each player contributes to the overall team offense. This percentage is then applied to the same metrics that the upcoming defense is allowing on average. The result is a points projection that takes into consideration how much a player contributes to their team as well as if that performance is likely to be affected negatively or postively based on their upcoming opponent. 

Upon running you will be prompted to enter the current week of the NFL season. This matches players with their upcoming opponents.

#### **Notes:**
+ The earliest you should run this for the upcoming week is the Tuesday before.This is because FantasyPros and FootballDB update at different times with FantasyPros doing one big update usually on Tuesday and FootballDB updating almost immediately after games are completed. With games being played on Tuesdays now I'm not sure how FantasyPros will handle updating. You can always check if FantasyPros has updated by going to [their stats page](https://www.fantasypros.com/nfl/stats/qb) and looking at the number of games played in the 'G' column.
+ Individual performance averages are calculated based on how many games *the player* has particpated in and ***not*** how many games their team has played. This is to prevent players who are injured for multiple weeks from having their stats diluted for not playing. 

***Scripts that import this module***: [dfs_optim.py](https://github.com/NOLAgnarwhal/fantasy-football/blob/master/dfs_optim.py), [oic_csv.py](https://github.com/NOLAgnarwhal/fantasy-football/blob/master/oic_csv.py)
___
### [OIC to CSV](https://github.com/NOLAgnarwhal/fantasy-football/blob/master/oic_csv.py)
___
This is pretty straight-forward as it simply takes the metrics calculated in the [opponent implied ceiling](https://github.com/NOLAgnarwhal/fantasy-football/tree/master/opponent_implied_ceiling) and outputs it into CSV format. This is useful if you want to see raw stats on players' average performance, what percentage of offensive stats they contribute, or to look at opponent implied ceilings in a non-DataFrame format. Output is for the upcoming week. 
___

### [DFS Lineup Optimizer](https://github.com/NOLAgnarwhal/fantasy-football/blob/master/dfs_optim.py)
___
The DFS Lineup Optimizer (`dfs_optim.py`) uses my own [opponent implied ceiling](https://github.com/NOLAgnarwhal/fantasy-football/tree/master/opponent_implied_ceiling) projections combined with the current week's DraftKings slate to create the lineup with the most projected points given position and salary contraints. Once running `python3 dfs_optim.py` from the working directory you will be prompted to input the current week in the NFL season and any players you wish to exclude. The output is then shown in the terminal. 

#### **Notes:**
+ This uses my own projections with their pros and cons baked in. Feel free to input your own projections. 
+ The DK salaries csv in the code is hosted on my local machine. You will have to change that to where DK salaries are on your own machine. 

#### ***Upcoming Improvements (feel free to contribute!):***
+ Add DFS site flexibility. Right now this is hardcoded for the DraftKings classic lineup setup and uses PPR scoring for projections. 
+ Diversify projections. Maybe ceiling, median, floor? Maybe bootstrapping?
+ Add multi-lineup output functionality. Honestly have no clue how to do that at this point, but it'll be fun to learn.
___





