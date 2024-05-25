import os

from common.get_data import *
from indicators.moving_average import *
from indicators.trend_indicators import *
from indicators.bollinger_bands import *

company = {'name': 'VW', 'tickersymbol': 'VWAGY'}
df = get_last_years(years=4, company=company['tickersymbol'])

add_sma(df=df, window_size=50)
add_sma(df=df, window_size=200)
add_ema(df=df, n_smooth=10)
add_wma(df=df, window_size=5)
add_adx(df=df, n_smooth=14)
add_macd(df=df, fast=12, slow=26)
add_bbands(df=df, sma_window=20, factor=2)

plot_adx(path=f'{os.getcwd()}', df=df, company=company['name'], adx_num=14, strong_trend=25)
plot_average(path=f'{os.getcwd()}', df=df, company=company['name'], indicators=['SMA50', 'SMA200', 'EMA10', 'WMA5'])
plot_macd(path=f'{os.getcwd()}', df=df, company=company['name'], fast=12, slow=26)
plot_bbands(path=f'{os.getcwd()}', df=df, company=company['name'], sma_window=20, factor=2)
