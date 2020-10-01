#%%
import pandas as pd 
from pulp import *

dk_players = pd.read_csv('/home/gnarwhal/fantasy-football/dfs-optimization/salaries/DKSalaries-wk3-main-slate.csv')

flex_positions = ['RB', 'WR', 'TE']
dfs = []
for pos in flex_positions:  
    df = dk_players.loc[dk_players['Position'] == pos]
    dfs.append(df)

flex_players_df = pd.concat(dfs)
flex_players_df['Position'] = flex_players_df['Position'].replace(['RB','WR','TE'], 'FLEX')

dk_players = pd.concat([dk_players,flex_players_df])

dk_players = dk_players[['Position','Name','Salary','AvgPointsPerGame']] #Eventually will replace AvgPointsPerGame with own projections

salaries = {}
points = {}

for pos in dk_players['Position'].unique():
    available_pos = dk_players[dk_players['Position'] == pos]
    
    salary = list(available_pos[['Name','Salary']].set_index('Name').to_dict().values())[0]

    point = list(available_pos[['Name','AvgPointsPerGame']].set_index('Name').to_dict().values())[0]

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
# %%
