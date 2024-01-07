import os

from common.get_data import *
from indicators.moving_average import *
from indicators.trend_indicators import *


df = get_last_years(years=4, company='VWAGY')

add_sma(df=df, window_size=50)
add_sma(df=df, window_size=200)
add_ema(df=df, n_smooth=10)
add_wma(df=df, window_size=5)
add_adx(df=df, n_smooth=14)

plot_adx(path=f'{os.getcwd()}', df=df, company='VW', adx_num=14, strong_trend=25)
