import pandas as pd 
pd.set_option('precision', 2)
import numpy as np

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
        }, axis=1)

        df['PassYds/G'] = df['YDS'].iloc[:,0]/df['G']
        df['RushYds/G'] = df['YDS'].iloc[:,1]/df['G']
        df['PassTDs/G'] = df['TD'].iloc[:,0]/df['G']
        df['RushTDs/G'] = df['TD'].iloc[:,1]/df['G']
        df['Ints/G'] = df['Ints/G']/df['G']
        df['FumLost/G'] = df['FumLost/G']/df['G']

        df = df.drop(['YDS', 'TD'], axis=1)

        ordered_cols = ['Player', 'Team', 'Pos', 'PassYds/G', 'PassTDs/G',  'RushYds/G', 'RushTDs/G', 'Ints/G', 'FumLost/G', 'G']

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

nfl_sched_df = pd.read_csv('/home/gnarwhal/fantasy-football/opponent_implied_ceiling/nfl_sched.csv')

nfl_sched_df = nfl_sched_df.drop(['Unnamed: 0', 'Day',], axis=1)

nfl_sched_df = nfl_sched_df.loc[nfl_sched_df['Week']== week]

fpros_df = fpros_df.merge(nfl_sched_df, how='left', on='Team')

fbdb_url = 'https://www.footballdb.com/stats/teamstat.html?group={}&cat={}'
groupcat = [ ('D','T'), ('O','T'), ('D','P'), ('D','R'), ('O','R'), ('O','P')]
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

    if pair == groupcat[4]:
        df = df.rename({
            'TD':'TeamRushTDs/G',
            'Yds/G':'TeamRushYds/G'
        }, axis=1)
        df['TeamRushTDs/G'] = df['TeamRushTDs/G']/df['Gms']
        ordered_cols = ['Team','TeamRushYds/G','TeamRushTDs/G']
        df = df[ordered_cols]

    if pair == groupcat[5]:
        df = df.rename({
            'Cmp':'TeamRec/G',
            'Yds':'TeamRecYds/G',
            'TD':'TeamRecTDs/G',
        }, axis=1)
        df['TeamRec/G'] = df['TeamRec/G']/df['Gms']
        df['TeamRecYds/G'] = df['TeamRecYds/G']/df['Gms']
        df['TeamRecTDs/G'] = df['TeamRecTDs/G']/df['Gms']
        ordered_cols = ['Team','TeamRec/G','TeamRecYds/G','TeamRecTDs/G',]
        df = df[ordered_cols]
    
    if pair == groupcat[0] or pair == groupcat[4] or pair == groupcat[5]:
        fpros_df = pd.merge(fpros_df, df, how='left', on='Team')
    else:
        fbdb_dfs.append(df)

fbdb_df = fbdb_dfs[0]
fbdb_df = pd.merge(fbdb_df, fbdb_dfs[1], how='left', on='Team')
fbdb_df = pd.merge(fbdb_df, fbdb_dfs[2], how='left', on='Team')

fbdb_df = fbdb_df.rename({
    'Team':'Opp'
}, axis=1)
stats_df = pd.merge(fpros_df, fbdb_df, how='left', on='Opp')

off_fum_url = 'https://www.footballdb.com/stats/turnovers.html'
off_fum_table = pd.read_html(off_fum_url, attrs={'class':'statistics'})
off_fum_df = off_fum_table[0]
off_fum_df.columns = off_fum_df.columns.droplevel(level=0)
off_fum_df = off_fum_df.replace({
        'Team':fbdb_team_name_map
    })
off_fum_df = off_fum_df.rename({
    'Team':'Opp',
}, axis=1)
off_fum_df['OffFumLost/G'] = off_fum_df['Fum'].iloc[:,1]/off_fum_df['Gms']
off_fum_df['OffInt/G'] = off_fum_df['Int'].iloc[:,1]/off_fum_df['Gms']
ordered_cols = ['Opp','OffFumLost/G','OffInt/G']
off_fum_df = off_fum_df[ordered_cols]
stats_df = pd.merge(stats_df, off_fum_df, how='left', on='Opp')

off_sack_url = 'https://www.footballdb.com/stats/teamstat.html?group=O&cat=P'
off_sack_table = pd.read_html(off_sack_url, attrs={'class':'statistics'})
off_sack_df = off_sack_table[0]
off_sack_df = off_sack_df.replace({
    'Team':fbdb_team_name_map
})
off_sack_df = off_sack_df.rename({
    'Team':'Opp'
},axis=1)
off_sack_df['SackAllowed/G'] = off_sack_df['Sack']/off_sack_df['Gms']
ordered_cols = ['Opp','SackAllowed/G']
off_sack_df = off_sack_df[ordered_cols]
stats_df = pd.merge(stats_df, off_sack_df, how='left', on='Opp')

stats_df['%TeamPassYds/G'] = stats_df['PassYds/G']/stats_df['TeamRecYds/G']
stats_df['%TeamPassTDs/G'] = stats_df['PassTDs/G']/stats_df['TeamRecTDs/G']
stats_df['%TeamRushYds/G'] = stats_df['RushYds/G']/stats_df['TeamRushYds/G']
stats_df['%TeamRushTDs/G'] = stats_df['RushTDs/G']/stats_df['TeamRushTDs/G']
stats_df['%TeamRec/G'] = stats_df['Rec/G']/stats_df['TeamRec/G']
stats_df['%TeamRecYds/G'] = stats_df['RecYds/G']/stats_df['TeamRecYds/G']
stats_df['%TeamRecTDs/G'] = stats_df['RecTDs/G']/stats_df['TeamRecTDs/G']

stats_df['OI PassYds'] = stats_df['%TeamPassYds/G']*stats_df['PassYdsAllowed/G'] 
stats_df['OI PassTDs'] = stats_df['%TeamPassTDs/G']*stats_df['PassTDsAllowed/G'] 
stats_df['OI RushYds'] = stats_df['%TeamRushYds/G']*stats_df['RushingYdsAllowed/G']
stats_df['OI RushTDs'] = stats_df['%TeamRushTDs/G']*stats_df['RushingTDsAllowed/G']
stats_df['OI Rec'] = stats_df['%TeamRec/G']*stats_df['RecAllowed/G']
stats_df['OI RecYds'] = stats_df['%TeamRecYds/G']*stats_df['PassYdsAllowed/G']
stats_df['OI RecTDs'] = stats_df['%TeamRecTDs/G']*stats_df['PassTDsAllowed/G']

hppr_scoring_weights = {
    'PassYds/G': 0.04,
    'PassTDs/G': 4,
    'Ints/G': -1,
    'RushYds/G': 0.1,
    'RushTDs/G': 6,
    'Rec/G': 0.5,
    'RecYds/G': 0.1,
    'RecTDs/G': 6,
    'FumLost/G': -2,
}

hppr_oi_weights = {
    'OI PassYds': 0.04,
    'OI PassTDs': 4,
    'Ints/G': -1,
    'OI RushYds': 0.1,
    'OI RushTDs': 6,
    'OI Rec': 0.5,
    'OI RecYds': 0.1,
    'OI RecTDs': 6,
    'FumLost/G': -2,
}

ppr_scoring_weights = {
    'PassYds/G': 0.04,
    'PassTDs/G': 4,
    'Ints/G': -1,
    'RushYds/G': 0.1,
    'RushTDs/G': 6,
    'Rec/G': 1,
    'RecYds/G': 0.1,
    'RecTDs/G': 6,
    'FumLost/G': -2,
}

ppr_oi_weights = {
    'OI PassYds': 0.04,
    'OI PassTDs': 4,
    'Ints/G': -1,
    'OI RushYds': 0.1,
    'OI RushTDs': 6,
    'OI Rec': 1,
    'OI RecYds': 0.1,
    'OI RecTDs': 6,
    'FumLost/G': -2,
}

dst_scoring_weights = {
    'DefSack/G':1,
    'DefInt/G':2,
    'FR/G':2,
    'DefTD/G':6,
    'DefSafety/G':2
}

dst_oi_weights = {
    'SackAllowed/G':1,
    'OffInt/G':2,
    'OffFumLost/G':2,
}

def get_hppr_points(row):
    hppr_points = sum([row[column]*weight for column, weight in hppr_scoring_weights.items()])
    return hppr_points

def get_hppr_oi_points(row):
    hppr_oi_points = sum([row[column]*weight for column, weight in hppr_oi_weights.items()])
    return hppr_oi_points


def get_ppr_points(row):
    ppr_points = sum([row[column]*weight for column, weight in ppr_scoring_weights.items()])
    return ppr_points

def get_ppr_oi_points(row):
    ppr_oi_points = sum([row[column]*weight for column, weight in ppr_oi_weights.items()])
    return ppr_oi_points


def get_dst_points(row):
    dst_points = sum([row[column]*weight for column, weight in dst_scoring_weights.items()])
    return dst_points

def get_dst_oi_points(row):
    dst_oi_points = sum([row[column]*weight for column, weight in dst_oi_weights.items()])
    return dst_oi_points

dst_df = stats_df.loc[stats_df['Pos']=='DST']

dst_df['Avg Pts'] = dst_df.apply(get_dst_points, axis=1)
dst_df['OIC'] = dst_df.apply(get_dst_oi_points, axis=1)

dst_condlist = [dst_df['PtsAllowed/G']>=35, 
    ((dst_df['PtsAllowed/G']<35) & (dst_df['PtsAllowed/G']>=28)), 
    ((dst_df['PtsAllowed/G']<28) & (dst_df['PtsAllowed/G']>=21)),
    ((dst_df['PtsAllowed/G']<21) & (dst_df['PtsAllowed/G']>=14)),
    ((dst_df['PtsAllowed/G']<14) & (dst_df['PtsAllowed/G']>=7)),
    ((dst_df['PtsAllowed/G']<7) & (dst_df['PtsAllowed/G']>=1)), 
    dst_df['PtsAllowed/G']<1]
dst_choicelist = [dst_df['Avg Pts']-4,
    dst_df['Avg Pts']-1,
    dst_df['Avg Pts'],
    dst_df['Avg Pts']+1,
    dst_df['Avg Pts']+4,
    dst_df['Avg Pts']+7,
    dst_df['Avg Pts']+10]

dst_df['Avg Pts'] = np.select(dst_condlist, dst_choicelist)

dst_condlist = [dst_df['PtsScored/G']>=35, 
    ((dst_df['PtsScored/G']<35) & (dst_df['PtsScored/G']>=28)), 
    ((dst_df['PtsScored/G']<28) & (dst_df['PtsScored/G']>=21)),
    ((dst_df['PtsScored/G']<21) & (dst_df['PtsScored/G']>=14)),
    ((dst_df['PtsScored/G']<14) & (dst_df['PtsScored/G']>=7)),
    ((dst_df['PtsScored/G']<7) & (dst_df['PtsScored/G']>=1)), 
    dst_df['PtsScored/G']<1]
dst_choicelist = [dst_df['OIC']-4,
    dst_df['OIC']-1,
    dst_df['OIC'],
    dst_df['OIC']+1,
    dst_df['OIC']+4,
    dst_df['OIC']+7,
    dst_df['OIC']+10]

dst_df['OIC'] = np.select(dst_condlist, dst_choicelist)

ordered_cols = ['Player','Team','Pos','Week','Avg Pts','OIC','DefSack/G','DefInt/G','FR/G','DefTD/G','DefSafety/G','PtsAllowed/G','Opp','SackAllowed/G','OffFumLost/G','OffInt/G','PtsScored/G']
dst_df = dst_df[ordered_cols]
dst_df = dst_df.sort_values(by='OIC', ascending=False)

stats_df['HPPR Avg'] = stats_df.apply(get_hppr_points,axis=1)
stats_df['HPPR OIC'] = stats_df.apply(get_hppr_oi_points,axis=1)
stats_df['PPR Avg'] = stats_df.apply(get_ppr_points,axis=1)
stats_df['PPR OIC'] = stats_df.apply(get_ppr_oi_points,axis=1)

stats_df = stats_df.loc[stats_df['G']!=0]

qb_df = stats_df.loc[stats_df['Pos']=='QB'].fillna(0)
ordered_cols = ['Player','Team','Pos','Week','PPR Avg','PPR OIC','Opp','PassYds/G','OI PassYds','PassTDs/G','OI PassTDs','RushYds/G','OI RushYds','RushTDs/G','OI RushTDs','Ints/G','FumLost/G']
qb_df = qb_df[ordered_cols]
qb_df = qb_df.sort_values(by='PPR OIC', ascending=False)

rb_df = stats_df.loc[stats_df['Pos']=='RB'].fillna(0)
ordered_cols = ['Player','Team','Pos','Week','PPR Avg','PPR OIC','HPPR Avg','HPPR OIC','Opp','RushYds/G','OI RushYds','RushTDs/G','OI RushTDs','Rec/G', 'OI Rec','RecYds/G','OI RecYds','RecTDs/G','OI RecTDs','FumLost/G']
rb_df = rb_df[ordered_cols]
rb_df = rb_df.sort_values(by='PPR OIC', ascending=False)

wr_df = stats_df.loc[stats_df['Pos']=='WR'].fillna(0)
ordered_cols = ['Player','Team','Pos','Week','PPR Avg','PPR OIC','HPPR Avg','HPPR OIC','Opp','Rec/G', 'OI Rec','RecYds/G','OI RecYds','RecTDs/G','OI RecTDs','RushYds/G','OI RushYds','RushTDs/G','OI RushTDs','FumLost/G']
wr_df = wr_df[ordered_cols]
wr_df = wr_df.sort_values(by='PPR OIC', ascending=False)

te_df = stats_df.loc[stats_df['Pos']=='TE'].fillna(0)
ordered_cols = ['Player','Team','Pos','Week','PPR Avg','PPR OIC','HPPR Avg','HPPR OIC','Opp','Rec/G', 'OI Rec','RecYds/G','OI RecYds','RecTDs/G','OI RecTDs','RushYds/G','OI RushYds','RushTDs/G','OI RushTDs','FumLost/G']
te_df = te_df[ordered_cols]
te_df = te_df.sort_values(by='PPR OIC', ascending=False)

