#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:30:45 2020

@author: buku
"""

### ADP vs. Final PPR Points 2019-2020 Scatterplot Analysis ###
### TO DO ###
# Add labels to points with player names

import pandas as pd
from os import path
import matplotlib.pyplot as plt

data_dir = '/home/buku/Python/fantasy_football/data'

stats = pd.read_csv(path.join(data_dir, 'player_stats_2019.csv'))
### Columns we want are: 'Player', 'Tm', 'Pos', 'FantasyPoints', 'ADP'


### Make DataFrames for each position: RB, WR, TE, QBs
# Useful analysis is to df.isna().sum() to see how many players didn't make it within the top however many are represented in the DF

rbs = stats.loc[stats['Pos'] == 'RB', ['Player', 'Tm', 'Pos', 'FantasyPoints', 'ADP']]
wrs = stats.loc[stats['Pos'] == 'WR', ['Player', 'Tm', 'Pos', 'FantasyPoints', 'ADP']]
tes = stats.loc[stats['Pos'] == 'TE', ['Player', 'Tm', 'Pos', 'FantasyPoints', 'ADP']]
qbs = stats.loc[stats['Pos'] == 'QB', ['Player', 'Tm', 'Pos', 'FantasyPoints', 'ADP']]

### Choose columns to plot for each position
rb_pts = rbs['FantasyPoints']
rb_adp = rbs['ADP']

wr_pts = wrs['FantasyPoints']
wr_adp = wrs['ADP']

te_pts = tes['FantasyPoints']
te_adp = tes['ADP']

qb_pts = qbs['FantasyPoints']
qb_adp = qbs['ADP']



### Make scatter plot with all the fixins ###

### RBs ###
plt.scatter(rb_adp, rb_pts, color='blue', s=10)

plt.xlabel('ADP')
plt.ylabel('Total PPR Season Pts')
plt.title('Running Back ADP vs. Final PPR Points\n')
plt.xlim(left=0, right=170)
plt.ylim(bottom=-2, top=500)
plt.axhline(y=165.8, alpha=0.5)

#Lines that mark rounds
plt.axvspan(0, 12, fill=False, ec='blue', alpha=0.3)
plt.axvspan(12, 24, fill=False, ec='blue', alpha=0.3)
plt.axvspan(24, 36, fill=False, ec='blue', alpha=0.3)
plt.axvspan(36, 48, fill=False, ec='blue', alpha=0.3)
plt.axvspan(48, 60, fill=False, ec='blue', alpha=0.3)
plt.axvspan(60, 72, fill=False, ec='blue', alpha=0.3)
plt.axvspan(72, 84, fill=False, ec='blue', alpha=0.3)
plt.axvspan(84, 96, fill=False, ec='blue', alpha=0.3)
plt.axvspan(96, 108, fill=False, ec='blue', alpha=0.3)
plt.axvspan(108, 120, fill=False, ec='blue', alpha=0.3)
plt.axvspan(120, 132, fill=False, ec='blue', alpha=0.3)
plt.axvspan(132, 144, fill=False, ec='blue', alpha=0.3)
plt.axvspan(144, 156, fill=False, ec='blue', alpha=0.3)
plt.axvspan(156, 168, fill=False, ec='blue', alpha=0.3)

# "Rd X" labels at top
plt.text(1, 505, 'Rd 1', size=8)
plt.text(13, 505, 'Rd 2', size=8)
plt.text(25, 505, 'Rd 3', size=8)
plt.text(37, 505, 'Rd 4', size=8)
plt.text(49, 505, 'Rd 5', size=8)
plt.text(61, 505, 'Rd 6', size=8)
plt.text(73, 505, 'Rd 7', size=8)
plt.text(85, 505, 'Rd 8', size=8)
plt.text(97, 505, 'Rd 9', size=8)
plt.text(109, 505, 'Rd 10', size=7.5)
plt.text(121, 505, 'Rd 11', size=7.5)
plt.text(133, 505, 'Rd 12', size=7.5)
plt.text(145, 505, 'Rd 13', size=7.5)
plt.text(157, 505, 'Rd 14', size=7.5)
plt.text(115, 168, 'Median Totals Pts Top 50 RBs', size=7)

plt.savefig('/home/buku/Python/fantasy_football/figs/RB_adp_finalrank_scatter')
   
plt.show()

### WRs ###
plt.scatter(wr_adp, wr_pts, color='orange', s=10)

plt.xlabel('ADP')
plt.ylabel('Total PPR Season Pts')
plt.title('Wide Receiver ADP vs. Final PPR Points\n')
plt.xlim(left=0, right=170)
plt.ylim(bottom=-2, top=400)
plt.axhline(y=199.5, color='orange', alpha=0.5)

#Lines that mark rounds
plt.axvspan(0, 12, fill=False, ec='orange', alpha=0.3)
plt.axvspan(12, 24, fill=False, ec='orange', alpha=0.3)
plt.axvspan(24, 36, fill=False, ec='orange', alpha=0.3)
plt.axvspan(36, 48, fill=False, ec='orange', alpha=0.3)
plt.axvspan(48, 60, fill=False, ec='orange', alpha=0.3)
plt.axvspan(60, 72, fill=False, ec='orange', alpha=0.3)
plt.axvspan(72, 84, fill=False, ec='orange', alpha=0.3)
plt.axvspan(84, 96, fill=False, ec='orange', alpha=0.3)
plt.axvspan(96, 108, fill=False, ec='orange', alpha=0.3)
plt.axvspan(108, 120, fill=False, ec='orange', alpha=0.3)
plt.axvspan(120, 132, fill=False, ec='orange', alpha=0.3)
plt.axvspan(132, 144, fill=False, ec='orange', alpha=0.3)
plt.axvspan(144, 156, fill=False, ec='orange', alpha=0.3)
plt.axvspan(156, 168, fill=False, ec='orange', alpha=0.3)

# "Rd X" labels at top
plt.text(1, 405, 'Rd 1', size=8)
plt.text(13, 405, 'Rd 2', size=8)
plt.text(25, 405, 'Rd 3', size=8)
plt.text(37, 405, 'Rd 4', size=8)
plt.text(49, 405, 'Rd 5', size=8)
plt.text(61, 405, 'Rd 6', size=8)
plt.text(73, 405, 'Rd 7', size=8)
plt.text(85, 405, 'Rd 8', size=8)
plt.text(97, 405, 'Rd 9', size=8)
plt.text(109, 405, 'Rd 10', size=7.5)
plt.text(121, 405, 'Rd 11', size=7.5)
plt.text(133, 405, 'Rd 12', size=7.5)
plt.text(145, 405, 'Rd 13', size=7.5)
plt.text(157, 405, 'Rd 14', size=7.5)
plt.text(117, 202, 'Median Totals Pts Top 50 WRs', size=7)

plt.savefig('/home/buku/Python/fantasy_football/figs/WR_adp_finalrank_scatter')
      
plt.show()

### TEs ###
plt.scatter(te_adp, te_pts, color='green', s=10)

plt.xlabel('ADP')
plt.ylabel('Total PPR Season Pts')
plt.title('Tight End ADP vs. Final PPR Points\n')
plt.xlim(left=0, right=170)
plt.ylim(bottom=-2, top=300)
plt.axhline(y=129.9, color='green', alpha=0.5)

#Lines that mark rounds
plt.axvspan(0, 12, fill=False, ec='green', alpha=0.3)
plt.axvspan(12, 24, fill=False, ec='green', alpha=0.3)
plt.axvspan(24, 36, fill=False, ec='green', alpha=0.3)
plt.axvspan(36, 48, fill=False, ec='green', alpha=0.3)
plt.axvspan(48, 60, fill=False, ec='green', alpha=0.3)
plt.axvspan(60, 72, fill=False, ec='green', alpha=0.3)
plt.axvspan(72, 84, fill=False, ec='green', alpha=0.3)
plt.axvspan(84, 96, fill=False, ec='green', alpha=0.3)
plt.axvspan(96, 108, fill=False, ec='green', alpha=0.3)
plt.axvspan(108, 120, fill=False, ec='green', alpha=0.3)
plt.axvspan(120, 132, fill=False, ec='green', alpha=0.3)
plt.axvspan(132, 144, fill=False, ec='green', alpha=0.3)
plt.axvspan(144, 156, fill=False, ec='green', alpha=0.3)
plt.axvspan(156, 168, fill=False, ec='green', alpha=0.3)

# "Rd X" labels at top
plt.text(1, 305, 'Rd 1', size=8)
plt.text(13, 305, 'Rd 2', size=8)
plt.text(25, 305, 'Rd 3', size=8)
plt.text(37, 305, 'Rd 4', size=8)
plt.text(49, 305, 'Rd 5', size=8)
plt.text(61, 305, 'Rd 6', size=8)
plt.text(73, 305, 'Rd 7', size=8)
plt.text(85, 305, 'Rd 8', size=8)
plt.text(97, 305, 'Rd 9', size=8)
plt.text(109, 305, 'Rd 10', size=7.5)
plt.text(121, 305, 'Rd 11', size=7.5)
plt.text(133, 305, 'Rd 12', size=7.5)
plt.text(145, 305, 'Rd 13', size=7.5)
plt.text(157, 305, 'Rd 14', size=7.5)
plt.text(115, 132, 'Median Totals Pts Top 24 TEs', size=7)
    
plt.savefig('/home/buku/Python/fantasy_football/figs/TE_adp_finalrank_scatter')
 
plt.show()

### QBs ###
plt.scatter(qb_adp, qb_pts, color='purple', s=10)

plt.xlabel('ADP')
plt.ylabel('Total PPR Season Pts')
plt.title('Quarter Back ADP vs. Final PPR Points\n')
plt.xlim(left=0, right=170)
plt.ylim(bottom=-2, top=500)
plt.axhline(y=254.6, color='purple', alpha=0.5)

#Lines that mark rounds
plt.axvspan(0, 12, fill=False, ec='purple', alpha=0.3)
plt.axvspan(12, 24, fill=False, ec='purple', alpha=0.3)
plt.axvspan(24, 36, fill=False, ec='purple', alpha=0.3)
plt.axvspan(36, 48, fill=False, ec='purple', alpha=0.3)
plt.axvspan(48, 60, fill=False, ec='purple', alpha=0.3)
plt.axvspan(60, 72, fill=False, ec='purple', alpha=0.3)
plt.axvspan(72, 84, fill=False, ec='purple', alpha=0.3)
plt.axvspan(84, 96, fill=False, ec='purple', alpha=0.3)
plt.axvspan(96, 108, fill=False, ec='purple', alpha=0.3)
plt.axvspan(108, 120, fill=False, ec='purple', alpha=0.3)
plt.axvspan(120, 132, fill=False, ec='purple', alpha=0.3)
plt.axvspan(132, 144, fill=False, ec='purple', alpha=0.3)
plt.axvspan(144, 156, fill=False, ec='purple', alpha=0.3)
plt.axvspan(156, 168, fill=False, ec='purple', alpha=0.3)

# "Rd X" labels at top
plt.text(1, 505, 'Rd 1', size=8)
plt.text(13, 505, 'Rd 2', size=8)
plt.text(25, 505, 'Rd 3', size=8)
plt.text(37, 505, 'Rd 4', size=8)
plt.text(49, 505, 'Rd 5', size=8)
plt.text(61, 505, 'Rd 6', size=8)
plt.text(73, 505, 'Rd 7', size=8)
plt.text(85, 505, 'Rd 8', size=8)
plt.text(97, 505, 'Rd 9', size=8)
plt.text(109, 505, 'Rd 10', size=7.5)
plt.text(121, 505, 'Rd 11', size=7.5)
plt.text(133, 505, 'Rd 12', size=7.5)
plt.text(145, 505, 'Rd 13', size=7.5)
plt.text(157, 505, 'Rd 14', size=7.5)
plt.text(118, 256, 'Median Totals Pts Top 24 QBs', size=7)
   
plt.savefig('/home/buku/Python/fantasy_football/figs/QB_adp_finalrank_scatter')
    
plt.show()
