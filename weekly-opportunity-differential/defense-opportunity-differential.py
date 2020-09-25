#%%
import pandas as pd
import numpy as np

#The 'week' variable is used to slice the nfl_sched_df below into the appropriate week for purposes of identifying the week's opponent. This is needed later when team defense stats are scraped.
week = int(input('What week in the season is it?:'))

#Scrape FantasyPros Player Season Stats
fp_url = 'https://www.fantasypros.com/nfl/stats/{pos}.php?range=full'

positions = ['qb', 'rb', 'wr', 'te']
dfs = []
for pos in positions:
    table = pd.read_html(fp_url.format(pos=pos), attrs={'id':'data'})
    df = table[0]

    #Removes upper level of column headers
    df.columns = df.columns.droplevel(level=0)
    #Removes players who have not scored any fantasy points
    df = df[df['FPTS'] !=0]
    #Creates Pos, Team and Player columns
    df['Pos'] = pos.upper()
    
    df['Team'] = df['Player'].apply(lambda x: x.split()[-1].strip('()'))

    df['Player'] = df['Player'].apply(lambda x: ' '.join(x.split()[:-1]))

    #Maninpulate columns for QBs
    if pos == 'qb':
        df = df.rename({
            'INT':'Ints',
            'FL':'FumLost'
        }, axis=1)

        df['PassYds'] = df['YDS'].iloc[:,0]/df['G']
        df['RushYds'] = df['YDS'].iloc[:,1]/df['G']
        df['PassTDs'] = df['TD'].iloc[:,0]/df['G']
        df['RushTDs'] = df['TD'].iloc[:,1]/df['G']

        df = df.drop(['YDS', 'TD'], axis=1)

        ordered_cols = ['Player', 'Team', 'Pos', 'PassYds', 'PassTDs', 'Ints', 'RushYds', 'RushTDs', 'FumLost', 'G']

        df = df[ordered_cols]
    
    #Maninpulate columns for RBs
    elif pos == 'rb':
        df = df.rename({
            'REC':'Rec',
            'FL':'FumLost'
        }, axis=1)

        df['RushYds'] = df['YDS'].iloc[:,0]/df['G']
        df['RecYds'] = df['YDS'].iloc[:,1]/df['G']
        df['RushTDs'] = df['TD'].iloc[:,0]/df['G']
        df['RecTDs'] = df['TD'].iloc[:,1]/df['G']

        df.drop(['YDS', 'TD'], axis=1)

        ordered_cols = ['Player', 'Team', 'Pos','RushYds', 'RushTDs', 'Rec', 'RecYds', 'RecTDs', 'FumLost', 'G']

        df = df[ordered_cols]
    #Maninpulate columns for WRs and TEs
    elif pos == 'wr' or pos =='te':
        df = df.rename({
            'REC':'Rec',
            'FL':'FumLost'
        }, axis=1)

        df['RushYds'] = df['YDS'].iloc[:,1]/df['G']
        df['RecYds'] = df['YDS'].iloc[:,0]/df['G']
        df['RushTDs'] = df['TD'].iloc[:,1]/df['G']
        df['RecTDs'] = df['TD'].iloc[:,0]/df['G']

        df.drop(['YDS', 'TD'], axis=1)

        ordered_cols = ['Player', 'Team', 'Pos','RushYds', 'RushTDs', 'Rec', 'RecYds', 'RecTDs', 'FumLost', 'G']

        df = df[ordered_cols]
    
    #Append makes a list of all position dfs in the list called "dfs"
    dfs.append(df)

#Concat makes dfs list into one DF we'll call "opportunity_df"
opportunity_df = pd.concat(dfs).fillna(0)

### Add DST to opportunity_df. First we have to scrape FantasyPros and FootballDB for the applicable stats. Then we merge those two DFs and finally concat that onto opportunity_df.
fp_def_url = 'https://www.fantasypros.com/nfl/stats/dst.php?range=full'
fp_def_table = pd.read_html(fp_def_url, attrs={'id':'data'})
fp_def_df = fp_def_table[0]

#Creates Pos, Team and Player columns
fp_def_df['Pos'] = 'DST'    
fp_def_df['Team'] = fp_def_df['Player'].apply(lambda x: x.split()[-1].strip('()'))
fp_def_df['Player'] = fp_def_df['Player'].apply(lambda x: ' '.join(x.split()[:-1]))

fp_def_df = fp_def_df.drop([
    'FPTS','FPTS/G','OWN','FF'
], axis=1)

fp_def_df = fp_def_df.rename({
    'SACK':'Sack',
    'INT':'Int',
    'SFTY':'Safety'
}, axis=1)

fp_def_df['Def TD'] = fp_def_df['DEF TD']+fp_def_df['SPC TD']

fp_def_df = fp_def_df.drop([
    'DEF TD', 'SPC TD'
], axis=1)

fbdb_def_url = 'https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr=2020&type=reg&cat=T&group=D'
fbdb_def_table = pd.read_html(fbdb_def_url, attrs={'class':'statistics'})
fbdb_def_df = fbdb_def_table[0]

fbdb_team_name_map = {
    'Arizona CardinalsArizona':'ARI',
    'Atlanta FalconsAtlanta':'ATL',
    'Baltimore RavensBaltimore':'BAL',
    'Buffalo BillsBuffalo':'BUF',
    'Carolina PanthersCarolina':'CAR',
    'Chicago BearsChicago':'CHI',
    'Cincinnati BengalsCincinnati':'CIN',
    'Cleveland BrownsCleveland':'CLE',
    'Dallas CowboysDallas':'DAL',
    'Denver BroncosDenver':'DEN',
    'Detroit LionsDetroit':'DET',
    'Green Bay PackersGreen Bay':'GB',
    'Houston TexansHouston':'HOU',
    'Indianapolis ColtsIndianapolis':'IND',
    'Jacksonville JaguarsJacksonville':'JAC',
    'Kansas City ChiefsKansas City':'KC',
    'Las Vegas RaidersLas Vegas':'LV',
    'Los Angeles ChargersLA Chargers':'LAC',
    'Los Angeles RamsLA Rams':'LAR',
    'Miami DolphinsMiami':'MIA',
    'Minnesota VikingsMinnesota':'MIN',
    'New England PatriotsNew England':'NE',
    'New Orleans SaintsNew Orleans':'NO',
    'New York GiantsNY Giants':'NYG',
    'New York JetsNY Jets':'NYJ',
    'Philadelphia EaglesPhiladelphia':'PHI',
    'Pittsburgh SteelersPittsburgh':'PIT',
    'San Francisco 49ersSan Francisco':'SF',
    'Seattle SeahawksSeattle':'SEA',
    'Tampa Bay BuccaneersTampa Bay':'TB',
    'Tennessee TitansTennessee':'TEN',
    'Washington Football TeamWashington':'WAS'
}

fbdb_def_df = fbdb_def_df.replace({
    'Team':fbdb_team_name_map
})

fbdb_def_df = fbdb_def_df.loc[:,['Team','Pts/G']]

dst_df = pd.merge(fp_def_df,fbdb_def_df, how='left', on='Team')

dst_df = dst_df.drop(['Rank'], axis=1)

opportunity_df = pd.concat([opportunity_df,dst_df]).fillna(0)

#Now we'll add our weekly opponent. If you're running this from your own computer I suggest running 'nfl-sched.py' or downloading 'nfl_sched.csv' located in the same folder as this file in GitHub (ADD GITHUB LINK HERE). 'nfl-sched.py' uses the sportsreference package to create 'nfl_sched.csv'. ###

nfl_sched_df = pd.read_csv('/home/gnarwhal/fantasy-football/weekly-opportunity-differential/nfl_sched.csv')

nfl_sched_df = nfl_sched_df.drop(['Unnamed: 0', 'Day',], axis=1)

nfl_sched_df = nfl_sched_df.loc[nfl_sched_df['Week']== week]

opportunity_df = opportunity_df.merge(nfl_sched_df, how='left', on='Team')

#%%
### So far we've scraped the offensive average performances of each fantasy point category for each offensive player who has scored fantasy points and added the functionality of identifying the week's opponent through user input.###

### Next, we're going to figure out what percentage of players' stats account for the overall team offensive production. First we'll have to scrape overall offensive team data from The Football Database. ###

#Making Team Passing Offense DF
team_pass_url = 'https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr=2020&type=reg&cat=P&group=O&sort=teamname'
team_pass_table = pd.read_html(team_pass_url, attrs={'class':'statistics'})
team_pass_df = team_pass_table[0]

team_pass_df['TeamRec/G'] = team_pass_df['Cmp']/team_pass_df['Gms']
team_pass_df['TeamPassYds/G'] = team_pass_df['Yds']/team_pass_df['Gms']
team_pass_df['TeamPassTDs/G'] = team_pass_df['TD']/team_pass_df['Gms']
team_pass_df['TeamInts/G'] = team_pass_df['Int']/team_pass_df['Gms']

team_pass_df = team_pass_df.drop([
    'Cmp', 'Yds', 'TD', 'Int', 'Att', 'Pct', 'YPA', 'Sack', 'Loss', 'Rate', 'NetYds', 'Yds/G', 'Gms'
], axis=1)

#Making Team Rushing Offense DF
team_rush_url = 'https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr=2020&type=reg&cat=R&group=O&sort=teamname'
team_rush_table = pd.read_html(team_rush_url, attrs={'class':'statistics'})
team_rush_df = team_rush_table[0]

team_rush_df['TeamRushTDs/G'] = team_rush_df['TD']/team_rush_df['Gms']
team_rush_df['TeamRushYds/G'] = team_rush_df['Yds/G']

team_rush_df = team_rush_df.drop([
    'Att', 'Yds', 'Avg', 'FD', 'Yds/G', 'TD', 'Gms'
], axis=1)

#Merge Rushing and Passing Offense DFs and manipulate Team names to match Player Average DF

###This is also part where I think some regex would do for splitting the team_off_df Team column up, but not quite sure how.
team_off_df = pd.merge(team_pass_df, team_rush_df, on='Team')

team_off_df = team_off_df.replace({
    'Team':fbdb_team_name_map
})

#Merge Team Offense DF with Player Average DF so each player. Now each player has a team total associated with them.
opportunity_df = opportunity_df.merge(team_off_df, how='left', on='Team')

#Create a "% of [TEAM STAT]" column by dividing individual player average by total team average. Fillna takes care of some blank cells which were popping up.
opportunity_df['% of TeamPassYds'] = opportunity_df['PassYds']/opportunity_df['TeamPassYds/G']
opportunity_df['% of TeamPassYds'].fillna(0, inplace=True)

opportunity_df['% of TeamPassTDs'] = opportunity_df['PassTDs']/opportunity_df['TeamPassTDs/G']
opportunity_df['% of TeamPassTDs'].fillna(0, inplace=True)

opportunity_df['% of TeamInts'] = opportunity_df['Ints']/opportunity_df['TeamInts/G']
opportunity_df['% of TeamInts'].fillna(0, inplace=True)

opportunity_df['% of TeamRushYds'] = opportunity_df['RushYds']/opportunity_df['TeamRushYds/G']
opportunity_df['% of TeamRushYds'].fillna(0, inplace=True)

opportunity_df['% of TeamRushTDs'] = opportunity_df['RushTDs']/opportunity_df['TeamRushTDs/G']
opportunity_df['% of TeamRushTDs'].fillna(0, inplace=True)

opportunity_df['% of TeamRec'] = opportunity_df['Rec']/opportunity_df['TeamRec/G']
opportunity_df['% of TeamRec'].fillna(0, inplace=True)

opportunity_df['% of TeamRecYds'] = opportunity_df['RecYds']/opportunity_df['TeamPassYds/G']
opportunity_df['% of TeamRecYds'].fillna(0, inplace=True)

opportunity_df['% of TeamRecTDs'] = opportunity_df['RecTDs']/opportunity_df['TeamPassTDs/G']
opportunity_df['% of TeamRecTDs'].fillna(0, inplace=True)

### Now we're going to scrape team defensive stats for the opponent of the week and add those stats to the opportunity_df ###

#Making Team Passing Defense DF
pass_def_url = 'https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr=2020&type=reg&cat=P&group=D&sort=teamname'
pass_def_table = pd.read_html(pass_def_url, attrs={'class':'statistics'})
pass_def_df = pass_def_table[0]

pass_def_df['RecAllowed/G'] = pass_def_df['Cmp']/pass_def_df['Gms']
pass_def_df['PassYdsAllowed/G'] = pass_def_df['Yds']/pass_def_df['Gms']
pass_def_df['PassTDsAllowed/G'] = pass_def_df['TD']/pass_def_df['Gms']
pass_def_df['IntsCaused/G'] = pass_def_df['Int']/pass_def_df['Gms']

pass_def_df = pass_def_df.drop([
    'Cmp', 'Yds', 'TD', 'Int', 'Att', 'Pct', 'YPA', 'Sack', 'Loss', 'Rate', 'NetYds', 'Yds/G', 'Gms'
], axis=1)

pass_def_df = pass_def_df.rename({
    'Team':'Opp'
}, axis=1)

#Making Team Rushing Defense DF
rush_def_url = 'https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr=2020&type=reg&cat=R&group=D&sort=teamname'
rush_def_table = pd.read_html(rush_def_url, attrs={'class':'statistics'})
rush_def_df = rush_def_table[0]

rush_def_df['RushTDsAllowed/G'] = rush_def_df['TD']/rush_def_df['Gms']
rush_def_df['RushYdsAllowed/G'] = rush_def_df['Yds/G']

rush_def_df = rush_def_df.drop([
    'Att', 'Yds', 'Avg', 'FD', 'Yds/G', 'TD', 'Gms'
], axis=1)

rush_def_df = rush_def_df.rename({
    'Team':'Opp'
}, axis=1)

#Combining Passing and Rushing Team Defense DFs into Overall Team Defense DF and merging it with Player Average DF
team_def_df = pd.merge(pass_def_df, rush_def_df, on='Opp')

team_def_df = team_def_df.replace({
    'Opp':fbdb_team_name_map
})
opportunity_df = opportunity_df.merge(team_def_df, how='left', on='Opp')

### Now we're going to figure out a player's expected floor given the defense they are about to face. We're going to take the percent of a team's offense a player is responsible for and multiply that by how much of a stat the upcoming defense allows on average per game. 
#For example, let's say Alvin Kamara is responsible on average for 50% of the Saints' RushingYds and he's going to face the Falcons next whose defense allows on average 200 RushingYds. Alvin Kamara would have an Defensively Implied Upcoming Performance of 100 RushingYds. These columns will be labeled beginning with "DI" which will stand for "Defensively Implied"
#We'll use this later to compare to the player's Average Performance throughout the year and create an Opportunity Metric. ###

opportunity_df['DI PassYds'] = opportunity_df['% of TeamPassYds']*opportunity_df['PassYdsAllowed/G']

opportunity_df['DI PassTDs'] = opportunity_df['% of TeamPassTDs']*opportunity_df['PassTDsAllowed/G']

opportunity_df['DI Ints'] = opportunity_df['% of TeamInts']*opportunity_df['IntsCaused/G']

opportunity_df['DI RushYds'] = opportunity_df['% of TeamRushYds']*opportunity_df['RushYdsAllowed/G']

opportunity_df['DI RushTDs'] = opportunity_df['% of TeamRushTDs']*opportunity_df['RushTDsAllowed/G']

opportunity_df['DI Rec'] = opportunity_df['% of TeamRec']*opportunity_df['RecAllowed/G']

opportunity_df['DI RecYds'] = opportunity_df['% of TeamRecYds']*opportunity_df['PassYdsAllowed/G']

opportunity_df['DI RecTDs'] = opportunity_df['% of TeamRecTDs']*opportunity_df['PassTDsAllowed/G']

### Now we're going to add columns for half PPR and PPR scoring systems. The scoring systems will be multiplied by the player's season average. We'll call this "Average Performance". We'll also multipy the scoring systems by our Defensively Implied stats. We'll call this "Defense Ceiling"

### Oh my god there's got to be a way to not copy and paste all that. For loop of course, but how to apply when each scoring_weights variable is a dict? Make a dict of dicts?

#Scoring weights for each half PPR and PPR. You can add your own league's scoring systems in the same way. 
hppr_scoring_weights = {
    'PassYds': 0.04,
    'PassTDs': 4,
    'Ints': -1,
    'RushYds': 0.1,
    'RushTDs': 6,
    'Rec': 0.5,
    'RecYds': 0.1,
    'RecTDs': 6,
    'FumLost': -2,
}

ppr_scoring_weights = {
    'PassYds': 0.04,
    'PassTDs': 4,
    'Ints': -1,
    'RushYds': 0.1,
    'RushTDs': 6,
    'Rec': 1,
    'RecYds': 0.1,
    'RecTDs': 6,
    'FumLost': -2,
}

### Apply scoring weights to each league to create a unique Average Performance column based on each league's scoring weights

#Half PPR Average Performance
opportunity_df['HPPR Average Performance'] = (
    opportunity_df['PassYds']*hppr_scoring_weights['PassYds'] +
    opportunity_df['PassTDs']*hppr_scoring_weights['PassTDs'] +
    opportunity_df['Ints']*hppr_scoring_weights['Ints'] +
    opportunity_df['RushYds']*hppr_scoring_weights['RushYds'] +
    opportunity_df['RushTDs']*hppr_scoring_weights['RushTDs'] +
    opportunity_df['Rec']*hppr_scoring_weights['Rec'] +
    opportunity_df['RecYds']*hppr_scoring_weights['RecYds'] +
    opportunity_df['RecTDs']*hppr_scoring_weights['RecTDs'] +
    opportunity_df['FumLost']*hppr_scoring_weights['FumLost']
)
#Half PPR Defense Ceiling
opportunity_df['HPPR Defense Ceiling'] = (
    opportunity_df['DI PassYds']*hppr_scoring_weights['PassYds'] +
    opportunity_df['DI PassTDs']*hppr_scoring_weights['PassTDs'] +
    opportunity_df['DI Ints']*hppr_scoring_weights['Ints'] +
    opportunity_df['DI RushYds']*hppr_scoring_weights['RushYds'] +
    opportunity_df['DI RushTDs']*hppr_scoring_weights['RushTDs'] +
    opportunity_df['DI Rec']*hppr_scoring_weights['Rec'] +
    opportunity_df['DI RecYds']*hppr_scoring_weights['RecYds'] +
    opportunity_df['DI RecTDs']*hppr_scoring_weights['RecTDs'] 
)
#Half PPR Opportunity Differential
opportunity_df['HPPR Opportunity Differential'] = opportunity_df['HPPR Defense Ceiling']-opportunity_df['HPPR Average Performance']

#PPR Average Performance
opportunity_df['PPR Average Performance'] = (
    opportunity_df['PassYds']*ppr_scoring_weights['PassYds'] +
    opportunity_df['PassTDs']*ppr_scoring_weights['PassTDs'] +
    opportunity_df['Ints']*ppr_scoring_weights['Ints'] +
    opportunity_df['RushYds']*ppr_scoring_weights['RushYds'] +
    opportunity_df['RushTDs']*ppr_scoring_weights['RushTDs'] +
    opportunity_df['Rec']*ppr_scoring_weights['Rec'] +
    opportunity_df['RecYds']*ppr_scoring_weights['RecYds'] +
    opportunity_df['RecTDs']*ppr_scoring_weights['RecTDs'] +
    opportunity_df['FumLost']*ppr_scoring_weights['FumLost']
)
#PPR Defense Ceiling
opportunity_df['PPR Defense Ceiling'] = (
    opportunity_df['DI PassYds']*ppr_scoring_weights['PassYds'] +
    opportunity_df['DI PassTDs']*ppr_scoring_weights['PassTDs'] +
    opportunity_df['DI Ints']*ppr_scoring_weights['Ints'] +
    opportunity_df['DI RushYds']*ppr_scoring_weights['RushYds'] +
    opportunity_df['DI RushTDs']*ppr_scoring_weights['RushTDs'] +
    opportunity_df['DI Rec']*ppr_scoring_weights['Rec'] +
    opportunity_df['DI RecYds']*ppr_scoring_weights['RecYds'] +
    opportunity_df['DI RecTDs']*ppr_scoring_weights['RecTDs'] 
)
#PPR Opportunity Differential
opportunity_df['PPR Opportunity Differential'] = opportunity_df['PPR Defense Ceiling']-opportunity_df['PPR Average Performance']

opportunity_df.to_csv('Week {week} Opportunity Differentials.xlsx'.format(week=week))

# %%
#Now we're going to make a DF for each position including only the applicable stats. We'll use each of these DFs to make a separate tab on a spreadsheet we'll pump out at the end.

#%%
# split_dfs=[]
# for pos in opportunity_df['Pos']:
#     split_dfs = opportunity_df.groupby('Pos')

    
#%%
# qb_opportunity_df = split_dfs[0]
# rb_opportunity_df = split_dfs[1]
# te_opportunity_df = split_dfs[2]
# wr_opportunity_df = split_dfs[3]
# %%
# writer = pd.ExcelWriter('Week {week} Opportunity Differentials.xlsx'.format(week=week), engine='xlsxwriter')

# qb_opportunity_df.to_excel(writer, sheet_name='QB')
# rb_opportunity_df.to_excel(writer, sheet_name='RB')
# wr_opportunity_df.to_excel(writer, sheet_name='WR')
# te_opportunity_df.to_excel(writer, sheet_name='TE')

# writer.save()
# %%
