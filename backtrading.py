from fastquant import get_stock_data, backtest
from datetime import date

today = date.today()

df = get_stock_data("WFG.TO", "2015-09-01", today)

backtest('smac', df, fast_period=25, slow_period=52)

# res = backtest("smac", df, fast_period=range(10, 30, 3), slow_period=range(40, 55, 3), verbose=False)
# print(res[['fast_period', 'slow_period', 'final_value']].head())
#
