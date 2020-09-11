import pandas as pd
import numpy as np

#Reads large CSV file in 10000 rows or chunksizes and then concatenates it into larger DF
pbp_df = pd.read_csv('/home/gnarwhal/fantasy-football/data/play-by-play/pbp2009-2018.csv', iterator=True, low_memory=False, chunksize=10000)

df = pd.DataFrame()
for chunk in pbp_df:
    df = pd.concat([df, chunk])

#Check for relevant columns using keywords
#Comment out after column names are identified
# for column in df.columns:
#     if 'rush' in column:
#         print(column)
#     elif 'distance' in column:
#         print(column)
#     elif 'yardline' in column:
#         print(column)

#Creates rushing specific DF where rush_attempt is True and two_point_attempt is False
rushing_df = df[['rush_attempt', 'rush_touchdown', 'yardline_100', 'two_point_attempt']]

rushing_df = rushing_df.loc[(rushing_df['two_point_attempt']==0) & (rushing_df['rush_attempt']==1)]

#Groups by yardline of play and calculates the proportion of plays that resulted in touchdowns
rushing_df_probs = rushing_df.groupby('yardline_100')['rush_touchdown'].value_counts(normalize=True)

rushing_df_probs = pd.DataFrame({
    'probability_of_touchdown':rushing_df_probs.values
}, index=rushing_df_probs.index).reset_index()

#Gets rid of plays which did not result in touchdowns and drops the rush_touchdown column since we know we only want to look at rushing plays that resulted in a touchdown
rushing_df_probs = rushing_df_probs.loc[rushing_df_probs['rush_touchdown']==1]

rushing_df_probs = rushing_df_probs.drop('rush_touchdown', axis=1)

#This next bit of code makes a separate CSV out of the rushing_dfs_probs DF for data viz purposes. It will be commented out if unneeded.
# rushing_df_probs.to_csv('rushing-td-probability', index=False)

'''So far we have made a rushing_df_probs DF which has calculated the probability of a rushing touchdown being scored from certain yardage away from the endzone using data from 2008 to 2019. Now we're going to make a separate DF to analyze RBs in 2019'''

pbp_2019_df = pd.read_csv('/home/gnarwhal/fantasy-football/data/2019pbp.csv', 
                        iterator=True,
                        low_memory=False,
                        chunksize=10000,
                        index_col=0)

pbp_2019_df_final = pd.DataFrame()

for chunk in pbp_2019_df:
    pbp_2019_df_final = pd.concat([pbp_2019_df_final, chunk])

#Using unique shows that yardage only goes to the 50 yard line from the OPP or OWN yard line. Will need to adjust to make totals out of 100.
pbp_2019_df_final['YardLineFixed'].unique()
pbp_2019_df_final['YardLineDirection'].unique()

#Create a function that turns plays into a 100-yd value when on own side of field 
def fix_yardline(row):
    yardline = row['YardLineFixed']
    direction = row['YardLineDirection']

    if direction == 'OPP':
        return yardline
    else:
        return 100 - yardline

#Pare down DF to necessary columns and drop non-applicable rows
pbp_2019_df_final = pbp_2019_df_final[['RushingPlayer', 'OffenseTeam', 'YardLineFixed', 'YardLineDirection']]

pbp_2019_df_final = pbp_2019_df_final.dropna()

#Apply the fix_yardline function. Remember that it affects the 'YardLineFixed' based on what 'YardLineDirection' says and then makes a new column using .apply()
pbp_2019_df_final['yardline_100'] = pbp_2019_df_final.apply(fix_yardline, axis=1)

#Renames columns and drops now unnecessary columns. 
pbp_2019_df_final = pbp_2019_df_final.rename({
    'RushingPlayer':'Player',
    'OffenseTeam':'Tm'
}, axis=1).drop(['YardLineDirection','YardLineFixed'], axis=1)

#Merge 2019 play-by-play with the rushing probability from each yardline DF in order to give each player's play at each yardline a probability of scoring a touchdown. Remember, they share the 'yardline_100' column.
df = pbp_2019_df_final.merge(rushing_df_probs, how='left', on='yardline_100')

#Pare down the DF by unique players and teams. Use .agg() to np.sum together the probabilities for each player of making a touchdown. This will add up to be the number of Expected Touchdowns for the year
df = df.groupby(['Player', 'Tm'], as_index=False).agg({
    'probability_of_touchdown':np.sum
}).rename({'probability_of_touchdown':'Expected Touchdowns'}, axis=1)

df = df.sort_values(by='Expected Touchdowns', ascending=False)

df['Expected Touchdowns Rank'] = df['Expected Touchdowns'].rank(ascending=False)

#Import DF that uses actual 2019 results for Rushing TDs
stats_df = pd.read_csv('/home/gnarwhal/fantasy-football/data/yearly/2019.csv').iloc[:,1:][['Player', 'Tm', 'Pos', 'RushingTD']]

#Stats DF and Expected Touchdown DF uses two different sets of team name. The following three pieces of code help isolate which team names are different
# print('Differing Team Names:', list(set(stats_df['Tm'].unique()) - set(df['Tm'].unique())))

# print('stats_df Team Names:', stats_df['Tm'].unique().tolist())

# print('df Team Names:', df['Tm'].unique().tolist())


#Creating team_name_map with values of wanted team names allows us to use .replace() 
team_name_map = {
    'TAM':'TB',
    'KAN':'KC',
    'LAR':'LA',
    'NOR':'NO',
    'GNB':'GB',
    'NWE':'NE',
    'SFO':'SF'
}

stats_df = stats_df.replace({
    'Tm':team_name_map
})

#Since we'll be merging the two DFs based on Player Name and Team we have to also normalize the player names
def fix_player_names(name):
    name_split = name.split()

    first_initial = name_split[0][0].upper()

    last_name = name_split[1].upper()

    return '.'.join([first_initial, last_name])

stats_df['Player'] = stats_df['Player'].apply(fix_player_names)

stats_df = stats_df.loc[stats_df['Pos']=='RB']

#Merge 2019 Actual Touchdown totals in stats_df with Expected Touchdowns in df. Merge on Player and Tm columns
df = stats_df.merge(df, how='left', on=['Player', 'Tm']).dropna()

df = df.drop('Pos', axis=1)

df = df.rename({'RushingTD':'Actual Touchdowns'}, axis=1)

df['Actual Touchdowns Rank'] = df['Actual Touchdowns'].rank(ascending=False)

#Candidates for regression are calculated based on the difference between their Expected Touchdowns and their Actual Touchdowns. If that difference is positive that means they underperformed last season. If the difference is negative it means they overperformed last season.
df['Regression Candidate'] = df['Expected Touchdowns'] - df['Actual Touchdowns']

#The rank is calculated by the difference between Actual Touchdowns and Expected Touchdowns since we want ranking to be descending
df['Regression Rank Candidate'] = df['Actual Touchdowns'] - df['Expected Touchdowns Rank']

#Set a minimum threshold for Expected Touchdowns to weed out irrelevant players
df = df.loc[df['Expected Touchdowns']> 2]

#Save as CSV for use in plotting in separate python file
df.to_csv('rb-td-regression-candidates.csv', index=False)