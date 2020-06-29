#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:22:04 2020

@author: gnarwhal
"""
###Calculating Value Over Replacement
### Source: https://www.fantasyfootballdatapros.com/course/section/6

### TO DO
#use 2020 projections
#import my fantasy leagues' scoring systems as different columns
#align with VOLS instead of average of top 100

import pandas as pd

df = pd.read_csv('/home/gnarwhal/fantasy_football/data/2019.csv')

#drop unnecessary columns
df.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'], axis=1, inplace=True)

#fix name formatting
df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

#rename columns
df.rename({
    'TD': 'PassingTD',
    'TD.1': 'RushingTD',
    'TD.2': 'ReceivingTD',
    'TD.3': 'TotalTD',
    'Yds': 'PassingYDs',
    'Yds.1': 'RushingYDs',
    'Yds.2': 'ReceivingYDs',
    'Att': 'PassingAtt',
    'Att.1': 'RushingAtt'
    }, axis=1, inplace=True)

#create column that calculates Fantasy Points 
df['FantasyPoints'] = df['PassingYDs']/25 + df['PassingTD']*4 - df['Int']*2 + df['Rec']*0.5 + df['ReceivingYDs']/10 + df['ReceivingTD']*6 + df['RushingYDs']/10 + df['RushingTD']*6

#determines range of DF sorted by FantasyPoints
draft_pool_limit = 100

#determines average FantasyPoints scored for everyone in a position
def calculate_average_based_off_position(our_df, pos):
    return our_df[our_df['FantPos'] == pos]['FantasyPoints'].mean()

cabop = calculate_average_based_off_position

#sorts FantasyPoints high to low and limits output to draft_pool_limit
new_df = df.sort_values(by=['FantasyPoints'], ascending=False)[:draft_pool_limit]

#uses calc avg function passing a new position into new_df
rb_avg_replacement = cabop(new_df, 'RB')
wr_avg_replacement = cabop(new_df, 'WR')
te_avg_replacement = cabop(new_df, 'TE')
qb_avg_replacement = cabop(new_df, 'QB')

#creates dictionary to iterate over 
pos_replacement_vals = {
    'RB': rb_avg_replacement,
    'WR': wr_avg_replacement,
    'TE': te_avg_replacement,
    'QB': qb_avg_replacement
}

#recreates new_df from above into form with VOR calculated
#DF is empty at first - only gives column names - will be filled in by for loop
new_df = pd.DataFrame({}, columns=['Player', 'FantPos', 'FantasyPoints', 'VOR'])

#uses .items() to iterate over keys and values in dictionary above
for position, replacement_value in pos_replacement_vals.items():
    pos_df = df[df['FantPos'] == position]
    pos_df = pos_df[['Player', 'FantPos', 'FantasyPoints']]
    pos_df['VOR'] = pos_df['FantasyPoints'] - replacement_value
    new_df = pd.concat([new_df, pos_df])

new_df.sort_values(by=["VOR"], ascending=False).head(25)