import pandas as pd
import matplotlib.pyplot as plt


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
    tr14[14] = df['TR1'][1:15].sum()
    for i in range(15, len(df)):
        tr14[i] = tr14[i-1] - tr14[i-1]/14 + df.iloc[i]['TR1']
    df['TR14'] = tr14

    # Calculate DM14plus and DM14minus
    dm14minus = pd.Series(float("NaN"), index=df.index)
    dm14plus = pd.Series(float("NaN"), index=df.index)
    dm14minus[14] = df['DMminus'][1:15].sum()
    dm14plus[14] = df['DMplus'][1:15].sum()
    for i in range(15, len(df)):
        dm14minus[i] = dm14minus[i-1] - dm14minus[i-1]/14 + df.iloc[i]['DMminus']
        dm14plus[i] = dm14plus[i-1] - dm14plus[i-1]/14 + df.iloc[i]['DMplus']
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
    adx[28] = df['DX'][14:29].mean()
    for i in range(29, len(df)):
        adx[i] = (13 * adx[i-1] + df.iloc[i]['DX']) / 14
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

    fig, axs = plt.subplots(2, figsize=(20,5))
    fig.suptitle(f'ADX{adx_num} for Company {company}')
    for day in list(tmp_df.loc[tmp_df['crossover'] == 1].index) :
        if df.loc[day][f'ADX{adx_num}'] > strong_trend :
            axs[0].axvline(x=day, color='green', linestyle='--', linewidth=0.5)
            axs[1].axvline(x=day, color='green', linestyle='--', linewidth=0.5)
    for day in list(tmp_df.loc[tmp_df['crossover'] == -1].index) :
        if df.loc[day][f'ADX{adx_num}'] > strong_trend :
            axs[0].axvline(x=day, color='red', linestyle='--', linewidth=0.5)
            axs[1].axvline(x=day, color='red', linestyle='--', linewidth=0.5)

    axs[0].plot(df.index, df['High'], label=f'{company} High', color='blue', linewidth=1)

    axs[1].axhline(y=week_trend, color='grey', linestyle='--', linewidth=0.5)
    axs[1].axhline(y=strong_trend, color='grey', linestyle='--', linewidth=0.5)
    axs[1].plot(df.index, df[f'DI{adx_num}plus'], label=f'+DI{adx_num}', color='green', linewidth=0.5)
    axs[1].plot(df.index, df[f'DI{adx_num}minus'], label=f'-DI{adx_num}', color='red', linewidth=0.5)
    axs[1].plot(df.index, df[f'ADX{adx_num}'], label=f'ADX{adx_num}', color='blue', linewidth=0.5)

    axs[0].set_xlim(left=df.index.min(), right=df.index.max())
    axs[1].set_xlim(left=df.index.min(), right=df.index.max())

    plt.legend()
    plt.savefig(f'{path}/ADX{adx_num}_{company}.pdf')
