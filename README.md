This repo is where I store data, visualizations and scripts pertaining to Fantasy Football.

# Working Projects

## [Opponent Implied Ceiling](https://github.com/NOLAgnarwhal/fantasy-football/tree/master/opponent_implied_ceiling)
Opponent Implied Ceiling (OIC) creates a points projection for fantasy players based on their upcoming matchups by scraping individual stats from FantasyPros and team stats from FootballDB. Average individual performance in fantasy point metrics are scraped and then compared with average overall team offense in the same categories to create a percentage each player contributes to the overall team offense. This percentage is then applied to the same metrics that the upcoming defense is allowing on average. The result is a points projection that takes into consideration how much a player contributes to their team as well as if that performance is likely to be affected negatively or postively based on their upcoming opponent. 

**Notes:**
+ The earliest you should run this for the upcoming week is the Tuesday before.This is because FantasyPros and FootballDB update at different times with FantasyPros doing one big update usually on Tuesday and FootballDB updating almost immediately after games are completed. With games being played on Tuesdays now I'm not sure how FantasyPros will handle updating. You can always check if FantasyPros has updated by going to [their stats page](https://www.fantasypros.com/nfl/stats/qb) and looking at the number of games played in the 'G' column.
+ Individual performance averages are calculated based on how many games *the player* has particpated in and ***not*** how many games their team has played.This is to prevent players who are injured for multiple weeks from having their stats diluted for not playing. 