import pandas as pd
import numpy as np


def add_adx(df: pd.core.frame.DataFrame, n_smooth: int = 14) :
    """
    """
    assert n_smooth == 14, f'Not implemented.'
    assert len(df) > 2*n_smooth+2, f'At least {2*n_smooth+2} trading days for ADX{n_smooth} needed.'

    # UpMove = Curr High - Prev High
    # DownMove = Prev Low - Curr Low
    temp_df = pd.DataFrame(index=df.index)
    temp_df['UpMove'] = df['High'] - df.shift(1)['High']
    temp_df['DownMove'] = df.shift(1)['Low'] - df['Low']

    # DMplus = UpMove if UpMove > DownMove and UpMove > 0, else: DMplus = 0
    # DMminus = DownMove if DownMove > Upmove and Downmove > 0, else DMminus = 0
    df['DMplus']  = temp_df.iloc[1:].apply(lambda row: row['UpMove'] if row['UpMove'] > row['DownMove'] and row['UpMove'] > 0 else 0.0, axis=1)
    df['DMminus'] = temp_df.iloc[1:].apply(lambda row: row['DownMove'] if row['DownMove'] > row['UpMove'] and row['DownMove'] > 0 else 0.0, axis=1)

    # Calculate True Range (TR)
    temp_df['Th_Tl'] = df['High'] - df['Low']
    temp_df['Th_Yc'] = df['High'] - df.shift(1)['Close']
    temp_df['Tl_Yc'] = df['Low'] - df.shift(1)['Close']
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

    # Calculate DI14plus and DI14minus
    # DI14minus = DM14minus/TR14, DI14plus = DM14plus/TR14
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
