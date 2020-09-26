#%%
import pandas as pd 
import itertools

week = int(input('What week of the NFL season is it?: '))

fp_url = 'https://www.fantasypros.com/nfl/stats/{pos}.php?range=full'


positions = ['qb','rb','wr','te','dst']
dfs = []
for pos in positions:
    table = pd.read_html(fp_url.format(pos=pos), attrs={'id':'data'})
    df = table[0]

    if pos != 'dst':
        df.columns = df.columns.droplevel(level=0)
    
    df['Pos'] = pos.upper()
    df['Team'] = df['Player'].apply(lambda x: x.split()[-1].strip('()'))
    df['Player'] = df['Player'].apply(lambda x: ' '.join(x.split()[:-1]))

    if pos == 'qb':
        df = df.rename({
            'INT':'Ints/G',
            'FL':'FumLost/G',
            'SACKS':'Sacked/G'
        }, axis=1)

        df['PassYds/G'] = df['YDS'].iloc[:,0]/df['G']
        df['RushYds/G'] = df['YDS'].iloc[:,1]/df['G']
        df['PassTDs/G'] = df['TD'].iloc[:,0]/df['G']
        df['RushTDs/G'] = df['TD'].iloc[:,1]/df['G']
        df['Ints/G'] = df['Ints/G']/df['G']
        df['FumLost/G'] = df['FumLost/G']/df['G']
        df['Sacked/G'] = df['Sacked/G']/df['G']

        df = df.drop(['YDS', 'TD'], axis=1)

        ordered_cols = ['Player', 'Team', 'Pos', 'PassYds/G', 'PassTDs/G',  'RushYds/G', 'RushTDs/G', 'Ints/G', 'Sacked/G','FumLost/G', 'G']

        df = df[ordered_cols]
    
    elif pos == 'rb':
        df = df.rename({
            'REC':'Rec/G',
            'FL':'FumLost/G'
        }, axis=1)

        df['RushYds/G'] = df['YDS'].iloc[:,0]/df['G']
        df['RecYds/G'] = df['YDS'].iloc[:,1]/df['G']
        df['RushTDs/G'] = df['TD'].iloc[:,0]/df['G']
        df['RecTDs/G'] = df['TD'].iloc[:,1]/df['G']
        df['Rec/G'] = df['Rec/G']/df['G']
        df['FumLost/G'] = df['FumLost/G']/df['G']

        df.drop(['YDS', 'TD'], axis=1)
    
        ordered_cols = ['Player', 'Team', 'Pos','RushYds/G', 'RushTDs/G', 'Rec/G', 'RecYds/G', 'RecTDs/G', 'FumLost/G', 'G']

        df = df[ordered_cols]

    elif pos == 'wr' or pos =='te':
        df = df.rename({
            'REC':'Rec/G',
            'FL':'FumLost/G'
        }, axis=1)

        df['RushYds/G'] = df['YDS'].iloc[:,1]/df['G']
        df['RecYds/G'] = df['YDS'].iloc[:,0]/df['G']
        df['RushTDs/G'] = df['TD'].iloc[:,1]/df['G']
        df['RecTDs/G'] = df['TD'].iloc[:,0]/df['G']
        df['Rec/G'] = df['Rec/G']/df['G']
        df['FumLost/G'] = df['FumLost/G']/df['G']

        df.drop(['YDS', 'TD'], axis=1)

        ordered_cols = ['Player', 'Team', 'Pos','RushYds/G', 'RushTDs/G', 'Rec/G', 'RecYds/G', 'RecTDs/G', 'FumLost/G', 'G']

        df = df[ordered_cols]

    elif pos == 'dst':
        df = df.rename({
            'SACK':'DefSack/G',
            'INT':'DefInt/G',
            'FR':'FR/G',
            'SFTY':'DefSafety/G'
        }, axis=1)

        df['DefSack/G'] = df['DefSack/G']/df['G']
        df['DefInt/G'] = df['DefInt/G']/df['G']
        df['FR/G'] = df['FR/G']/df['G']
        df['DefTD/G'] = (df['DEF TD']+df['SPC TD'])/df['G']
        df['DefSafety/G'] = df['DefSafety/G']/df['G']

        df.drop(['FF','DEF TD','SPC TD','FPTS','FPTS/G','OWN'], axis=1)
        
        ordered_cols = ['Player','Team','Pos','DefSack/G','DefInt/G','FR/G','DefTD/G','DefSafety/G']

        df = df[ordered_cols]

    dfs.append(df)

fpros_df = pd.concat(dfs).fillna(0)

#%%
nfl_sched_df = pd.read_csv('/home/gnarwhal/fantasy-football/opponent-implied-ceiling/nfl_sched.csv')

nfl_sched_df = nfl_sched_df.drop(['Unnamed: 0', 'Day',], axis=1)

nfl_sched_df = nfl_sched_df.loc[nfl_sched_df['Week']== week]

fpros_df = fpros_df.merge(nfl_sched_df, how='left', on='Team')

# %%
fbdb_url = 'https://www.footballdb.com/stats/teamstat.html?group={}&cat={}'
groupcat = [ ('D','T'), ('O','T'), ('D','P'), ('D','R')]
fbdb_dfs = []
for pair in groupcat:
    table = pd.read_html(fbdb_url.format(pair[0],pair[1]), attrs={'class':'statistics'})
    df = table[0]

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
    df = df.replace({
        'Team':fbdb_team_name_map
    })

    if pair == groupcat[0]:
        df = df.rename({
            'Pts/G':'PtsAllowed/G'
        }, axis=1)
        ordered_cols = ['Team','PtsAllowed/G']
        df = df[ordered_cols]
        fpros_df = pd.merge(fpros_df, df, how='left', on='Team')  

    if pair == groupcat[2]:
        df = df.rename({
            'Cmp':'RecAllowed/G',
            'Yds':'PassYdsAllowed/G',
            'TD':'PassTDsAllowed/G',
        }, axis=1)
        df['RecAllowed/G'] = df['RecAllowed/G']/df['Gms']
        df['PassYdsAllowed/G'] = df['PassYdsAllowed/G']/df['Gms']
        df['PassTDsAllowed/G'] = df['PassTDsAllowed/G']/df['Gms']
        ordered_cols = ['Team','RecAllowed/G','PassYdsAllowed/G','PassTDsAllowed/G']
        df = df[ordered_cols]
        
    
    if pair == groupcat[3]:
        df = df.rename ({
            'Yds/G':'RushingYdsAllowed/G',
            'TD':'RushingTDsAllowed/G',
        }, axis =1)
        df['RushingTDsAllowed/G'] = df['RushingTDsAllowed/G']/df['Gms']
        ordered_cols = ['Team','RushingYdsAllowed/G','RushingTDsAllowed/G']
        df = df[ordered_cols]
    
    
    if pair == groupcat[1]:
        df = df.rename({
            'Pts/G':'PtsScored/G'
        }, axis=1)
        ordered_cols = ['Team','PtsScored/G']
        df = df[ordered_cols]
    

    if pair != groupcat[0]:
        fbdb_dfs.append(df)
#%%
fbdb_df = fbdb_dfs[0]
fbdb_df = pd.merge(fbdb_df, fbdb_dfs[1], how='left', on='Team')
fbdb_df = pd.merge(fbdb_df, fbdb_dfs[2], how='left', on='Team')

# %%
fbdb_df = fbdb_df.rename({
    'Team':'Opp'
}, axis=1)
fpros_df = pd.merge(fpros_df, fbdb_df, how='left', on='Opp')
# %%
