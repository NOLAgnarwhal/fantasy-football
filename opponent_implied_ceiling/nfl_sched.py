from sportsreference.nfl.teams import Teams
import pandas as pd 

dfs = []
for team in Teams():
    schedule = team.schedule
    df = schedule.dataframe
    df['Team'] = team.abbreviation
    dfs.append(df)

nfl_sched_df = pd.concat(dfs)
nfl_sched_df = nfl_sched_df.sort_values(by='week')

sched_name_map = {
    'CLT' : 'IND',
    'CRD' : 'ARI',
    'GNB' : 'GB',
    'HTX' : 'HOU',
    'JAX' : 'JAC',
    'KAN' : 'KC',
    'NOR' : 'NO',
    'NWE' : 'NE',
    'OTI' : 'TEN',
    'RAI' : 'LV',
    'RAM' : 'LAR',
    'RAV' : 'BAL',
    'SDG' : 'LAC',
    'SFO' : 'SF',
    'TAM' : 'TB',
}

nfl_sched_df = nfl_sched_df.replace({
    'Team': sched_name_map,
    'opponent_abbr': sched_name_map
})

nfl_sched_df = nfl_sched_df.rename({
    'opponent_abbr': 'Opp',
    'day':'Day',
    'week':'Week'
}, axis=1)

nfl_sched_df = nfl_sched_df.loc[:,['Team', 'Opp', 'Day', 'Week']]

nfl_sched_df.to_csv('/home/gnarwhal/fantasy-football/weekly-stats/nfl_sched.csv')
