import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from indicators.moving_average import *


def add_bbands(df: pd.core.frame.DataFrame, sma_window: int = 20, factor: int = 2) :
    """Bollinger Bands can be an indicator of market volatility.
    Based on the normal distribution, it is assumed that current stock prices are more likely to be close to the mean value of past prices than far away from it.
    """
    if not f'SMA{sma_window}' in df.columns :
        add_sma(df=df, window_size=sma_window)
    
    sigma = np.sqrt(((df['Close'] - df[f'SMA{sma_window}'])**2).sum(skipna=True) / sma_window)
    sigma = (df['Close'] - df[f'SMA{sma_window}']).rolling(window=sma_window).std()
    
    df[f'BBand-upper-{sma_window}-{factor}'] = df[f'SMA{20}'] + factor * sigma
    df[f'BBand-lower-{sma_window}-{factor}'] = df[f'SMA{20}'] - factor * sigma


def plot_bbands(path: str, df: pd.core.frame.DataFrame, company: str, sma_window: int = 20, factor: int = 2) :
    """Plot Bollinger Bands for one company.
    The range of the Bollinger Bands correlates with market volatility.
    This is because the standard deviation increases when price ranges widen and decreases when they narrow.
    In volatile markets, the Bollinger Bands widen, while in less volatile markets, they narrow.
    Another part of the interpretation relates to whether the market is currently overbought or oversold.
    For example:
    Price reaches the upper band -> overbought area -> price falls
    Price reaches the lower band -> oversold area -> price rises
    """    
    plt.figure(figsize=(15,5))
    plt.title(f'Bollinger Bands SMA-{sma_window} Factor-{factor} for company {company}')

    upper_band = f'BBand-upper-{sma_window}-{factor}'
    lower_band = f'BBand-lower-{sma_window}-{factor}'
    plt.plot(df.index, df[upper_band], label=upper_band, linewidth=0.5, color='orange')
    plt.plot(df.index, df[lower_band], label=lower_band, linewidth=0.5, color='orange')
    plt.fill_between(df.index, df[lower_band], df[upper_band], color='gold', alpha=0.1)
    
    plt.bar(x=df.index, height=df['High']-df['Low'], bottom=df['Low'], color='blue', label=f'{company} Chart')
    plt.plot(df.index, (df['High'] + df['Low']) / 2, linewidth=0.5, color='blue')
    plt.plot(df.index, df[f'SMA{sma_window}'], label=f'SMA{sma_window}', linewidth=0.5, color='red')

    plt.xlim(left=df.index.min(), right=df.index.max())
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'{path}/BollingerBands_{company}.pdf')
