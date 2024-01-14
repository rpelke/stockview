import pandas as pd
import matplotlib.pyplot as plt

from indicators.moving_average import *


def add_macd(df: pd.core.frame.DataFrame, fast: int = 12, slow: int = 26) :
    """The Moving Average Convergence/Divergence (MACD) indicator is a trend-following tool in market analysis.
    It calculates the difference between two exponential moving averages and is often used with a signal line (trigger line) for analysis.
    MACD(default) = EMA(12)-EMA(26).
    The signal line is a 9-period EMA of the MACD.
    """
    if not f'EMA{fast}' in df.columns :
        add_ema(df=df, n_smooth=fast)
    if not f'EMA{slow}' in df.columns :
        add_ema(df=df, n_smooth=slow)

    col = f'MACD{fast}-{slow}'
    df[col] = df[f'EMA{fast}'] - df[f'EMA{slow}']
    
    add_ema(df=df, n_smooth=9, refcol=col, colname=f'{col}-trigger-{9}')


def plot_macd(path: str, df: pd.core.frame.DataFrame, company: str, fast: int = 12, slow: int = 26) :
    """Plot MACD for one company.
    Both the signal line and MACD are represented as lines in a two-line model.
    A rising MACD indicates an uptrend, while a falling MACD indicates a downtrend.
    A buying signal occurs when the MACD crosses its signal line from below.
    A selling signal occurs when the MACD crosses its signal line from above.
    The distance of the MACD from its centerline signals the strength of the trend.
    Increasing distance indicates stronger trends.
    A very large distance may suggest overbought/oversold conditions, potentially leading to trend reversals.
    If the gap between the signal line and the MACD widens, the trend strengthens; if it narrows, the trend weakens.
    Divergences between the MACD and its base (price series on which the MACD is calculated) can be interpreted as a possible signal for an impending trend reversal.
    """    
    fig, axs = plt.subplots(2, figsize=(15,5))
    fig.suptitle(f'MACD{fast}-{slow} for company {company}')

    axs[0].bar(x=df.index, height=df['High']-df['Low'], bottom=df['Low'], color='blue', label=f'{company} Chart')
    
    axs[1].axhline(y=0, color='grey', linewidth=0.2, linestyle='--')
    axs[1].plot(df.index, df[f'MACD{fast}-{slow}'], label=f'MACD{fast}-{slow}', color='blue', linewidth=0.5)
    axs[1].plot(df.index, df[f'MACD{fast}-{slow}-trigger-{9}'], label=f'MACD{fast}-{slow}-trigger-{9}', color='red', linewidth=0.5)
    
    tmp_df = pd.DataFrame(index=df.index)
    tmp_df['diff_pos'] = df.apply(lambda row: row[f'MACD{fast}-{slow}'] - row[f'MACD{fast}-{slow}-trigger-{9}'] if row[f'MACD{fast}-{slow}'] - row[f'MACD{fast}-{slow}-trigger-{9}'] > 0 else 0, axis=1)
    tmp_df['diff_neg'] = df.apply(lambda row: row[f'MACD{fast}-{slow}'] - row[f'MACD{fast}-{slow}-trigger-{9}'] if row[f'MACD{fast}-{slow}'] - row[f'MACD{fast}-{slow}-trigger-{9}'] < 0 else 0, axis=1)
    axs[1].bar(x=df.index, height=tmp_df['diff_pos'], color='blue', label=f'Positive diff')
    axs[1].bar(x=df.index, height=tmp_df['diff_neg'], color='orange', label=f'Negative diff')

    axs[0].set_xlim(left=df.index.min(), right=df.index.max())
    axs[1].set_xlim(left=df.index.min(), right=df.index.max())

    axs[0].legend(loc='upper left')
    axs[1].legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(f'{path}/MACD{fast}-{slow}_{company}.pdf')


def add_adx(df: pd.core.frame.DataFrame, n_smooth: int = 14) :
    """The Average Directional Index (ADX) signals market direction, trend presence, and momentum.
    +DI higher suggests an upward trend, while a greater -DI indicates a downward trend.
    ADX values above 20 confirm a trend.
    We currently use an EMA over 14 trading days.
    """
    assert n_smooth == 14, f'Not implemented.'
    assert len(df) > 2*n_smooth+2, f'At least {2*n_smooth+2} trading days for ADX{n_smooth} needed.'

    # UpMove = Curr High - Prev High
    # DownMove = Prev Low - Curr Low
    temp_df = pd.DataFrame(index=df.index)
    temp_df['UpMove'] = df['High'] - df['High'].shift(1)
    temp_df['DownMove'] = df['Low'].shift(1) - df['Low']

    # DMplus = UpMove if UpMove > DownMove and UpMove > 0, else: DMplus = 0
    # DMminus = DownMove if DownMove > Upmove and Downmove > 0, else DMminus = 0
    df['DMplus']  = temp_df.iloc[1:].apply(lambda row: row['UpMove'] if row['UpMove'] > row['DownMove'] and row['UpMove'] > 0 else 0.0, axis=1)
    df['DMminus'] = temp_df.iloc[1:].apply(lambda row: row['DownMove'] if row['DownMove'] > row['UpMove'] and row['DownMove'] > 0 else 0.0, axis=1)

    # Calculate True Range (TR)
    temp_df['Th_Tl'] = df['High'] - df['Low']
    temp_df['Th_Yc'] = df['High'] - df['Close'].shift(1)
    temp_df['Tl_Yc'] = df['Low'] - df['Close'].shift(1)
    df['TR1'] = temp_df.iloc[1:].apply(lambda row: max(row['Th_Tl'], abs(row['Th_Yc']), abs(row['Tl_Yc'])), axis=1)
    
    # First TR14: Sum of first 14 TR1
    # Subsequent TR14 = Prior TR14 - (Prior TR14/14) + Current TR1
    tr14 = pd.Series(float("NaN"), index=df.index)
    tr14.iloc[14] = df['TR1'][1:15].sum()
    for i in range(15, len(df)):
        tr14.iloc[i] = tr14.iloc[i-1] - tr14.iloc[i-1]/14 + df.iloc[i]['TR1']
    df['TR14'] = tr14

    # Calculate DM14plus and DM14minus
    dm14minus = pd.Series(float("NaN"), index=df.index)
    dm14plus = pd.Series(float("NaN"), index=df.index)
    dm14minus.iloc[14] = df['DMminus'][1:15].sum()
    dm14plus.iloc[14] = df['DMplus'][1:15].sum()
    for i in range(15, len(df)):
        dm14minus.iloc[i] = dm14minus.iloc[i-1] - dm14minus.iloc[i-1]/14 + df.iloc[i]['DMminus']
        dm14plus.iloc[i] = dm14plus.iloc[i-1] - dm14plus.iloc[i-1]/14 + df.iloc[i]['DMplus']
    df['DM14minus'] = dm14minus
    df['DM14plus'] = dm14plus

    # Calculate Directional Indicators (DI) +DI (DI14plus) and -DI (DI14minus)
    df['DI14minus'] = 100 * df['DM14minus'] / df['TR14']
    df['DI14plus'] = 100 * df['DM14plus'] / df['TR14']

    # Calculate Directional Movement Index (DX)
    # DX = ABS[(+DI14 - -DI14) / (+DI14 + -DI14)].
    df['DX'] = 100 * abs((df['DI14plus'] - df['DI14minus']) / (df['DI14plus'] + df['DI14minus']))

    # First ADX14: Mean of first 14 DX
    # Subsequent ADX14: ((Prior ADX14 * 13) + Current DX Value)/14
    adx = pd.Series(float("NaN"), index=df.index)
    adx.iloc[28] = df['DX'][14:29].mean()
    for i in range(29, len(df)):
        adx.iloc[i] = (13 * adx.iloc[i-1] + df.iloc[i]['DX']) / 14
    df[f'ADX{n_smooth}'] = adx


def plot_adx(path: str, df: pd.core.frame.DataFrame, company: str, adx_num: int = 14, week_trend: int = 20, strong_trend: int = 25) :
    """Plot stock value, ADX, +DI, and -DI for one company.
    Week trend: strong_trend > ADX > week_trend.
    Strong trend: ADX > strong_trend. Otherwise: No trend.
    Crossovers of the -DI and +DI lines can be used to generate trade signals.
    For example, if the +DI line crosses above the -DI line and the ADX is above 20, or ideally above 25, then that is a potential signal to buy.
    On the other hand, if the -DI crosses above the +DI, and the ADX is above 20 or 25, then that is an opportunity to enter a potential short trade.
    """
    tmp_df = pd.DataFrame(index=df.index)
    tmp_df['diff'] = df.apply(lambda row: 1 if row[f'DI{adx_num}plus'] > row[f'DI{adx_num}minus'] else 0, axis=1)
    tmp_df['crossover'] = tmp_df['diff'] - tmp_df['diff'].shift(1)

    fig, axs = plt.subplots(2, figsize=(15,5))
    fig.suptitle(f'ADX{adx_num} for company {company}')
    for day in list(tmp_df.loc[tmp_df['crossover'] == 1].index) :
        if df.loc[day][f'ADX{adx_num}'] > strong_trend :
            axs[0].axvline(x=day, color='green', linestyle='--', linewidth=0.5)
            axs[1].axvline(x=day, color='green', linestyle='--', linewidth=0.5)
    for day in list(tmp_df.loc[tmp_df['crossover'] == -1].index) :
        if df.loc[day][f'ADX{adx_num}'] > strong_trend :
            axs[0].axvline(x=day, color='red', linestyle='--', linewidth=0.5)
            axs[1].axvline(x=day, color='red', linestyle='--', linewidth=0.5)

    axs[0].bar(x=df.index, height=df['High']-df['Low'], bottom=df['Low'], color='blue', label=f'{company} Chart')

    axs[1].axhline(y=week_trend, color='grey', linestyle='--', linewidth=0.5)
    axs[1].axhline(y=strong_trend, color='grey', linestyle='--', linewidth=0.5)
    axs[1].plot(df.index, df[f'DI{adx_num}plus'], label=f'+DI{adx_num}', color='green', linewidth=0.5)
    axs[1].plot(df.index, df[f'DI{adx_num}minus'], label=f'-DI{adx_num}', color='red', linewidth=0.5)
    axs[1].plot(df.index, df[f'ADX{adx_num}'], label=f'ADX{adx_num}', color='blue', linewidth=0.5)

    axs[0].set_xlim(left=df.index.min(), right=df.index.max())
    axs[1].set_xlim(left=df.index.min(), right=df.index.max())

    axs[0].legend(loc='upper left')
    axs[1].legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'{path}/ADX{adx_num}_{company}.pdf')
