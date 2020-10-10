import pandas as pd 
from pulp import *
from opponent_implied_ceiling import opponent_implied_ceiling

excluded_players = []
dont_play = input('Players to exclude (click Enter when done): ')
while not dont_play == '':
    excluded_players.append(dont_play)
    dont_play = input('Players to exclude (click Enter when done): ')

opponent_implied_ceiling.dst_df['Player'] = opponent_implied_ceiling.dst_df['Player'].apply(lambda x: x.split()[-1])

wash_name = {
    'Team':'WAS Football Team'
}

opponent_implied_ceiling.dst_df = opponent_implied_ceiling.dst_df.replace({'Player':wash_name})

dfs = [opponent_implied_ceiling.qb_df, opponent_implied_ceiling.wr_df, opponent_implied_ceiling.rb_df, opponent_implied_ceiling.te_df, opponent_implied_ceiling.dst_df]

for df in dfs:
    points_df = pd.concat(dfs).fillna(0)

points_df['Name'] = points_df['Player']
ordered_cols = ['Name', 'PPR OIC']
points_df = points_df[ordered_cols]

player_name_map = {
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

points_df = points_df.replace({'Name':player_name_map})

dk_players = pd.read_csv('/home/gnarwhal/fantasy_football/dfs_optimization/salaries/wk{week}DKSalaries.csv'.format(week=opponent_implied_ceiling.week))

dk_players['Name'] = dk_players['Name'].apply(lambda x: x.strip())

dk_players = dk_players.merge(points_df, how='left', on='Name').fillna(0)

for player in excluded_players:
    dk_players = dk_players.loc[dk_players['Name']!=player]
#%%
#%%
flex_positions = ['RB', 'WR', 'TE']
dfs = []
for pos in flex_positions:  
    df = dk_players.loc[dk_players['Position'] == pos]
    dfs.append(df)

flex_players_df = pd.concat(dfs)
flex_players_df['Position'] = flex_players_df['Position'].replace(['RB','WR','TE'], 'FLEX')

dk_players = pd.concat([dk_players,flex_players_df])

dk_players = dk_players[['Position','Name','Salary','PPR OIC']] 

salaries = {}
points = {}

for pos in dk_players['Position'].unique():
    available_pos = dk_players[dk_players['Position'] == pos]
    
    salary = list(available_pos[['Name','Salary']].set_index('Name').to_dict().values())[0]

    point = list(available_pos[['Name','PPR OIC']].set_index('Name').to_dict().values())[0]

    salaries[pos] = salary
    points[pos] = point

pos_num_available = {
    'QB':1,
    'RB':2,
    'WR':3,
    'TE':1,
    'FLEX':1,
    'DST':1
}

salary_cap = 50000

_vars = {k: LpVariable.dict(k, v, cat='Binary') for k, v in points.items()}

prob = LpProblem('DFS Optimization', LpMaximize)
rewards = []
costs = []
position_constraints = []

for k, v in _vars.items():
    costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])
    rewards += lpSum([points[k][i] * _vars[k][i] for i in v])
    prob += lpSum([_vars[k][i] for i in v]) <= pos_num_available[k]

prob += lpSum(rewards)
prob += lpSum(costs) <= salary_cap

prob.solve()

def summary(prob):
    div = '---------------------------------------\n'
    print("Variables:\n")
    score = str(prob.objective)
    constraints = [str(const) for const in prob.constraints.values()]
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            print(v.name, "=", v.varValue)
    print(div)
    print("Constraints:")
    for constraint in constraints:
        constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
        if constraint_pretty != "":
            print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
    print(div)
    print("Score:")
    score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
    print("{} = {}".format(score_pretty, eval(score)))

print(summary(prob))

