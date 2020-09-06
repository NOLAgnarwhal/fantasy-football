import pandas as pd

df = pd.read_csv('/home/gnarwhal/fantasy-football/data/fantasypros/fp_projections.csv')

# Get rid of extra index column
df = df.iloc[:,1:]


#Customize FantasyPoints column to league scoring
scoring_weights = {
    'receptions': 0.5, 
    'receiving_yds': 0.1,
    'receiving_td': 6,
    'FL': -2, 
    'rushing_yds': 0.1,
    'rushing_td': 6,
    'passing_yds': 0.04,
    'passing_td': 4,
    'int': -1
}

#Replace FantasyPoints column with custom scoring weights
df['FantasyPoints'] = (
    df['Receptions']*scoring_weights['receptions'] 
    + df['ReceivingYds']*scoring_weights['receiving_yds'] 
    + df['ReceivingTD']*scoring_weights['receiving_td'] 
    + df['FL']*scoring_weights['FL'] 
    + df['RushingYds']*scoring_weights['rushing_yds'] 
    + df['RushingTD']*scoring_weights['rushing_td'] 
    + df['PassingYds']*scoring_weights['passing_yds'] 
    + df['PassingTD']*scoring_weights['passing_td'] 
    +df['Int']*scoring_weights['int'] 
    )

#Use ADP data to create a dictionary which contains the last player for each position to be drafted out of the top 100 drafted players. These are "replacement players"
adp_df = pd.read_csv('/home/gnarwhal/fantasy-football/data/fantasypros/adp/HALF_PPR_ADP.csv', index_col=0)

adp_df['ADP RANK'] = adp_df['AVG'].rank()

adp_df_cutoff = adp_df[:100]

replacement_players = {
    'RB': '',
    'QB': '',
    'WR': '',
    'TE': ''
}

for _, row in adp_df_cutoff.iterrows():

    position= row['POS']
    player = row['PLAYER']

    if position in replacement_players:
        replacement_players[position] = player


df = df[['Player', 'Pos', 'Team', 'FantasyPoints']]

replacement_values = {}

#Creates a new dictionary from replacement_players dict with the FantasyPoints column values for each player
for position, player_name in replacement_players.items():
    player = df.loc[df['Player'] == player_name]
    replacement_values[position] = player['FantasyPoints'].tolist()[0]

pd.set_option('chained_assignment', None)

#Pare down DF to only positions listed below
df = df.loc[df['Pos'].isin(['QB', 'RB', 'WR', 'TE'])]


#Create VOR column which subtracts replacement_values from FantasyPoints
df['VOR'] = df.apply(
    lambda row: row['FantasyPoints'] - replacement_values.get(row['Pos']), axis=1
)

pd.set_option('display.max_rows', None)

#Creates VOR Rank column and sorts DF by VOR
df['VOR Rank'] = df['VOR'].rank(ascending=False)

#Normalizes VOR between values of 0 and 1
df['VOR'] = df['VOR'].apply(lambda x: (x - df['VOR'].min())/(df['VOR'].max()-df['VOR'].min()))

df = df.sort_values(by='VOR Rank')

df = df.rename({
    'VOR': 'Value',
    'VOR Rank': 'Value Rank'
}, axis=1)


#Join ADP DF with VOR DF to look for gaps between ADP and Value
adp_df = adp_df.rename({
    'PLAYER': 'Player',
    'POS': 'Pos',
    'AVG': 'Average ADP',
    'ADP RANK': 'ADP Rank'
}, axis=1)

final_df = df.merge(adp_df, how='left', on=['Player', 'Pos'])

final_df['Diff in ADP and Value'] = final_df['ADP Rank'] - final_df['Value Rank']

"""At this point we have a DF with all positions ranked by VOR Value Rank. We can use pd.to_csv or to_excel right above this comment to save that. Below here we will calculate sleepers and overvalued players for each position and finally save each DF we make as separate sheets into one Excel workbook."""

num_of_teams = 12
num_of_spots = 16

#Make new DF which represents the league's draft pool. 
draft_pool = final_df.sort_values(by='ADP Rank')[:num_of_teams*num_of_spots]

#Create new DFs based off of position
rb_draft_pool = draft_pool.loc[draft_pool['Pos']== 'RB']
qb_draft_pool = draft_pool.loc[draft_pool['Pos']== 'QB']
wr_draft_pool = draft_pool.loc[draft_pool['Pos']== 'WR']
te_draft_pool = draft_pool.loc[draft_pool['Pos']== 'TE']

#Create sleeper DFs by sorting positional DF by highest difference in ADP and Value
rb_sleepers = rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
qb_sleepers = qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
wr_sleepers = wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
te_sleepers = te_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]

#Create overvalued DFs by sorting positional DF by lowest difference in ADP and Value
rb_overvalued = rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]
qb_overvalued = qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]
wr_overvalued = wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]
te_overvalued = te_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]

#Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter('VoR_cakewalk_draft_day.xlsx', engine='xlsxwriter')

#Take each DF and save it main Excel workbook (defined by "writer" variable) as a separate sheet
final_df.to_excel(writer, sheet_name='VoR')
rb_sleepers.to_excel(writer, sheet_name='RB Sleepers')
qb_sleepers.to_excel(writer, sheet_name='QB Sleepers')
wr_sleepers.to_excel(writer, sheet_name='WR Sleepers')
te_sleepers.to_excel(writer, sheet_name='TE Sleepers')
rb_overvalued.to_excel(writer, sheet_name='RB Overvalued')
qb_overvalued.to_excel(writer, sheet_name='QB Overvalued')
wr_overvalued.to_excel(writer, sheet_name='WR Overvalued')
te_overvalued.to_excel(writer, sheet_name='TE Overvalued')

#Close Pandas Excel writer and output Excel file
writer.save()