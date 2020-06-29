#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 02:34:40 2020

@author: gnarwhal
"""
### Calculates Values over Last Starter metric based on FantasyPros season fantasy points projections
# Source: https://www.fantasypros.com/nfl/projections/qb.php?week=draft

### TO DO
# Code in removing blank first line in WR, QB, RB, TE csvs
# Use variables to allow for expansion of code for 10 team, 2QB team, different scoring systems
# Tweak 'replacement' baseline model

import pandas as pd

### Path, file stem and file endings are concatenated and put into a list
DATA_DIR = '/home/gnarwhal/fantasy_football/data/'
csv_end = ['_DST.csv', '_K.csv', '_QB.csv', '_RB.csv', '_TE.csv', '_WR.csv']
file_stem = 'FantasyPros_Fantasy_Football_Projections'

proj_file = []
for end in csv_end:
    csv = DATA_DIR+file_stem+end
    proj_file.append(csv)

### Iterate over file paths in proj_file to create multiple DFs
dfs = []
for file_path in proj_file:
    df = pd.read_csv(file_path)
    dfs.append(df)

### Create dict with keys as positions and values as dfs
positions = ['DST', 'K', 'QB', 'RB', 'TE', 'WR']
df_dict = dict(zip(positions, dfs))
DST, K, QB, RB, TE, WR = df_dict.values()

### Iterate over dict to add Value over Last Starter column
for k, v in df_dict.items():
    if k == 'WR':
        v['VoLS'] = v['FPTS'] - v['FPTS'][23]
    elif k == 'RB':
        v['VoLS'] = v['FPTS'] - v['FPTS'][23]
    else:
        v['VoLS'] = v['FPTS'] - v['FPTS'][11]

        
vols_df = pd.DataFrame({}, columns=['Player', 'Team', 'POS', 'FPTS', 'VOLS'])

for values in df_dict.values():
    vols_df = pd.concat([vols_df, values])
    
vols_columns = ['Player', 'Team', 'POS', 'FPTS', 'VOLS']
vols_df = vols_df[vols_columns].sort_values(by='VOLS', ascending=False).reset_index(drop=True)

vols_df.to_csv('/home/gnarwhal/fantasy_football/data/VoLS.csv', index=False)



