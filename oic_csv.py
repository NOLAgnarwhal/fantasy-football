import pandas as pd
from opponent_implied_ceiling import opponent_implied_ceiling

writer = pd.ExcelWriter('opponent_implied_ceiling/csv/Week {week} OIC.xlsx'.format(week=opponent_implied_ceiling.week), engine='xlsxwriter')

opponent_implied_ceiling.qb_df.to_excel(writer, sheet_name='qb_df')
opponent_implied_ceiling.rb_df.to_excel(writer, sheet_name='rb_df')
opponent_implied_ceiling.wr_df.to_excel(writer, sheet_name='wr_df')
opponent_implied_ceiling.te_df.to_excel(writer, sheet_name='te_df')
opponent_implied_ceiling.dst_df.to_excel(writer, sheet_name='dst_df')

writer.save()
