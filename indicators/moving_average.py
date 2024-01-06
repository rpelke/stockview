import pandas as pd
import numpy as np


def add_sma(df: pd.core.frame.DataFrame, window_size: int) :
    """Add SMA to DataFrame
    The Simple Moving Average (SMA) is an arithmetic mean commonly used as a window_size=50 or window_size=200-day moving average.
    It smoothens short-term price movements by summing the closing prices of the previous 49 (199) days and the current closing price, dividing the total by 50 (200).
    This process creates a continuous series of average values, revealing the long-term trend of a security.
    """
    assert len(df) > window_size, f'At least {window_size} trading days for SMA{window_size} needed.'
    df[f'SMA{window_size}'] = df['Close'].rolling(window=window_size, min_periods=window_size).mean()


def add_ema(df: pd.core.frame.DataFrame, n_smooth: int) :
    """Add EMA to DataFrame
    SF (Smoothing Factor) = 2/ (n_smooth + 1)
    EMA(t) = C(t) * SF + (1 - SF) * EMA(t-1)
    """
    sf = 2 / (n_smooth + 1)

    ema = pd.Series(0.0, index=df.index)
    ema[0] = df.iloc[0]['Close']
    for i in range(1, len(df)):
        ema[i] = df.iloc[i]['Close'] * sf + (1 - sf) * ema[i-1]
    
    df[f'EMA{n_smooth}'] = ema


def add_wma(df: pd.core.frame.DataFrame, window_size: int) :
    """Add WMA to DataFrame
    A Weighted Moving Average (WMA) assigns greater significance to recent data by multiplying each price with a weighted factor.
    This distinctive calculation results in the WMA closely tracking prices compared to a SMA.
    WMA(t) = (c(t) * W(n) + c/t-1) * W(n-1) +...+ c(t-n+1) * W(n-n+1)) / (W(1) + W(2)+...+ W(n))
    c: 'Close' value, Weight factors W(x) = X
    """
    assert len(df) > window_size, f'At least {window_size} trading days for WMA{window_size} needed.'

    def _rolling_multiply(window) :
        wz = len(window) + 1
        return sum(window * range(1, wz)) / sum(range(1, wz))
    
    df[f'WMA{window_size}'] = df['Close'].rolling(window=window_size, min_periods=window_size).apply(_rolling_multiply, raw=True)
