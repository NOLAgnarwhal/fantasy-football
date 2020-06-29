#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:59:49 2020

@author: gnarwhal
"""

### TO DO
# Expand to all positions
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv('/home/gnarwhal/fantasy_football/data/2019.csv')

#drop unneccessary columns
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

df['Usage'] = df['PassingAtt'] + df['RushingAtt'] + df['Tgt']
df['Usage/GM'] = df['Usage']/df['G']

df['FantasyPoints'] = df['PassingYDs']/25 + df['PassingTD']*4 + df['Int']*-2 + df['RushingYDs']/10 + df['RushingTD']*6 + df['ReceivingYDs']/10 + df['Rec'] + df['ReceivingTD']*6 - df['FL']*2
df['FantasyPoints/GM'] = df['FantasyPoints']/df['G']

#separate dataframes based off position
rb_df = df[df['FantPos'] == 'RB']
qb_df = df[df['FantPos'] == 'QB']
wr_df = df[df['FantPos'] == 'WR']
te_df = df[df['FantPos'] == 'TE']

#Isolate columns that will pertain to certain positions
rushing_columns = ['RushingAtt', 'RushingYDs', 'Y/A', 'RushingTD']
receiving_columns = ['Tgt', 'Rec', 'ReceivingYDs', 'Y/R', 'ReceivingTD']
passing_columns = ['PassingAtt', 'PassingYDs', 'PassingTD', 'Int']

#Make a run a function that adds isolated columns to pertinent position
def transform_columns(df, new_column_list):
    df = df[['Player', 'Tm', 'G'] + new_column_list + ['FL']]
    return df

rb_df = transform_columns(rb_df, rushing_columns+receiving_columns)
wr_df = transform_columns(wr_df, rushing_columns+receiving_columns)
te_df = transform_columns(te_df, receiving_columns)
qb_df = transform_columns(qb_df, passing_columns)

#Create new column to calc points scored (PPR)
rb_df['FantasyPoints'] = (rb_df['RushingYDs']*0.1 + rb_df['RushingTD']*6 + rb_df['Rec'] + rb_df['ReceivingYDs']*0.1 + rb_df ['ReceivingTD']*6 - rb_df['FL']*2)

#Create new column to calc pts per game
rb_df['FantasyPoints/GM'] = rb_df['FantasyPoints']/rb_df['G']
rb_df['FantasyPoints/GM'] = rb_df['FantasyPoints/GM'].apply(lambda x: round(x,2))

#Create new column for usage
rb_df['Usage/GM'] = (rb_df['RushingAtt'] + rb_df['Tgt'])/rb_df['G']
rb_df['Usage/GM'] = rb_df['Usage/GM'].apply(lambda x: round(x, 2))

#Sets seaborn style
sns.set_style('whitegrid')

#.supblots() is like making the background canvas
fig, ax = plt.subplots()
fig.set_size_inches(20,20)

#Regression scatter plot with trendline
#plot = sns.regplot(rb_df['Usage/GM'], rb_df['FantasyPoints/GM'], scatter=True)

# #sns.scatterplot(x='Usage/GM', 
#                 y='FantasyPoints/GM', 
#                 data=df, 
#                 hue='FantPos', 
#                 size='FantasyPoints',
#                 )

#sns.lmplot(data=df, x='Usage/GM', y='FantasyPoints/GM', hue='FantPos', height=10, col='FantPos')

# sns.residplot(data=df, x='Usage/GM', y='FantasyPoints/GM')

#sns.jointplot(x='Usage/GM', y='FantasyPoints/GM', data=df, kind='reg')

#sns.pairplot(rb_df, x_vars=['RushingAtt', 'RushingYDs', 'Y/A', 'RushingTD', 'Tgt', 'Rec', 'ReceivingYDs', 'Y/R', 'ReceivingTD'], y_vars=['FantasyPoints/GM'], height=5, aspect=.8, kind='reg') 

















