import pandas as pd

page = 'https://www.footballdb.com/transactions/injured-reserve.html?sortfld=date&sortdir=desc#'

IR_table = pd.read_html(page, attrs={'class':'statistics'})

IR_df = IR_table[0]

IR_df.to_csv('Current_IR.csv')

