#%%
import pandas as pd
from matplotlib import pyplot as plt 

df = pd.read_csv('rushing-td-probability')

df.plot(x='yardline_100', y='probability_of_touchdown')

#Use to show in IDE. Will need to insert "#%%" at top of code
# plt.show()

plt.savefig('rushing-td-probability.png', bbox_inches='tight')




# %%
