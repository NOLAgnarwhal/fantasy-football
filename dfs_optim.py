import pandas as pd 
import pulp
from opponent_implied_ceiling import opponent_implied_ceiling
import re

### Adds unwanted players to a list. List used to delete players from DF later on. ###
excluded_players = []
dont_play = input('Players to exclude (click Enter when done): ')
while not dont_play == '':
    excluded_players.append(dont_play)
    dont_play = input('Players to exclude (click Enter when done): ')

### OIC DF for DST doesn't match DK names. Most names except for Washington are at the [-1] index ###
opponent_implied_ceiling.dst_df['Player'] = opponent_implied_ceiling.dst_df['Player'].apply(lambda x: x.split()[-1])
wash_name = {'Team':'WAS Football Team'}
opponent_implied_ceiling.dst_df = opponent_implied_ceiling.dst_df.replace({'Player':wash_name})

### Concat projection DFs and prep for merge with DK players DF ###
dfs = [opponent_implied_ceiling.qb_df, opponent_implied_ceiling.wr_df, opponent_implied_ceiling.rb_df, opponent_implied_ceiling.te_df, opponent_implied_ceiling.dst_df]

for df in dfs:
    proj_df = pd.concat(dfs).fillna(0)

proj_df['Name'] = proj_df['Player']
ordered_cols = ['Name', 'PPR OIC']
proj_df = proj_df[ordered_cols]

fix_player_name = { #will need to update manually weekly#
    'Patrick Mahomes II':'Patrick Mahomes',
    'D.J. Chark Jr.':'DJ Chark Jr.',
    'D.J. Moore':'DJ Moore',
    'Darrell Henderson':'Darrell Henderson Jr.',
    'Dwayne Haskins':'Dwayne Haskins Jr.',
    'Duke Johnson Jr.':'Duke Johnson',
    'Lamical Perine':"La'Mical Perine",
    'Wayne Gallman':'Wayne Gallman Jr.',
    'Steven Sims':'Steven Sims Jr.',
    'Chris Herndon IV':'Chris Herndon',
    'Van Jefferson':'Van Jefferson Jr.',
    'John Ross':'John Ross III',
}

proj_df = proj_df.replace({'Name':fix_player_name})

### Import DK player salary DF to merge with projections DF ###
dk_players = pd.read_csv('/home/gnarwhal/fantasy_football/salaries/wk{week}DKSalaries.csv'.format(week=opponent_implied_ceiling.week))
dk_players['Name'] = dk_players['Name'].apply(lambda x: x.strip()) #DK DF has white space for some reason#
dk_players = dk_players.merge(proj_df, how='left', on='Name').fillna(0)
dk_players = dk_players[['Position','Name','Salary','PPR OIC']] 

### Excludes players from list created at beginning with user input ###
for player in excluded_players:
    dk_players = dk_players.loc[dk_players['Name']!=player]

### Solve Optimization problem using puLP ###
player_data = dk_players.set_index('Name')

plist = dk_players['Name'].tolist()
qb = dk_players[dk_players['Position']=='QB']['Name'].tolist()
rb = dk_players[dk_players['Position']=='RB']['Name'].tolist()
wr = dk_players[dk_players['Position']=='WR']['Name'].tolist()
te = dk_players[dk_players['Position']=='TE']['Name'].tolist()
dst = dk_players[dk_players['Position']=='DST']['Name'].tolist()

prob = pulp.LpProblem('DFS Optimization', pulp.LpMaximize)
players = pulp.LpVariable.dicts('Player: ', plist, cat='Binary')
prob += pulp.lpSum([player_data['PPR OIC'][i] * players[i] for i in plist])
prob += pulp.lpSum([player_data['Salary'][i] * players[i] for i in plist]) <= 50000
prob += pulp.lpSum([players[i] for i in qb]) == 1
prob += pulp.lpSum([players[i] for i in rb]) >= 2
prob += pulp.lpSum([players[i] for i in wr]) >= 3
prob += pulp.lpSum([players[i] for i in te]) >= 1
prob += pulp.lpSum([players[i] for i in dst]) == 1
prob += pulp.lpSum([players[i] for i in plist]) == 9

prob.solve()

### Function prints output into terminal when script is run ###
def summary(prob):
    div = '---------------------------------------\n'
    print("Optimal Lineup:\n")
    score = str(prob.objective)
    constraints = [str(const) for const in prob.constraints.values()]
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            print(v.name, "=", v.varValue)
    print(div)
    print("Score:")
    score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
    print("{} = {}".format(score_pretty, eval(score)))

print(summary(prob))

