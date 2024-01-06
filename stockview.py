import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

from common.get_data import *
from indicators.moving_average import *

vw = yf.Ticker('VWAGY')
vw_hist = vw.history(period='3y')
tesla = yf.Ticker('TSLA')
tesla_hist = tesla.history(period='3y')

df = get_last_years(years=4, company='VWAGY')

add_sma(df=df, window_size=50)
add_sma(df=df, window_size=200)
add_ema(df=df, n_smooth=10)
add_wma(df=df, window_size=5)


### Plot
fig, ax1 = plt.subplots(figsize=(20,5))
ax2 = ax1.twinx()
ax1.plot(vw_hist.index, vw_hist["High"], label="VW High", color="blue", linewidth=0.5)
ax2.plot(tesla_hist.index, tesla_hist["High"], label="Tesla High", color="green", linewidth=0.5)
fig.legend()
fig.savefig("stock_hist_high.png")

fig, ax1 = plt.subplots(figsize=(20,5))
ax2 = ax1.twinx()
ax1.plot(vw_hist.index[1:], np.diff(vw_hist["High"]), label="VW High Diff", color="darkblue", linewidth=0.5)
ax2.plot(tesla_hist.index[1:], np.diff(tesla_hist["High"]), label="Tesla High Diff", color="darkgreen", linewidth=0.5)
ax1.axhline(y=0, color="darkblue")
ax2.axhline(y=0, color="darkgreen")
fig.legend()
fig.savefig("diff_hist_high.png")
