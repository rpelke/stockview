import yfinance as yf
import pandas as pd


def get_comp_stock_hist(company: str, period: str) -> pd.core.frame.DataFrame :
    yf_comp = yf.Ticker(company)
    return yf_comp.history(period=period)


def get_last_years(years: int, company: str) -> pd.core.frame.DataFrame :
    df = get_comp_stock_hist(company=company, period='max')
    tz_df = df.iloc[0].name.tz
    timestamp = pd.Timestamp.today(tz=tz_df) - pd.DateOffset(years=years)
    return df[df.index > timestamp]


def get_last_months(months: int, company: str) -> pd.core.frame.DataFrame :
    df = get_comp_stock_hist(company=company, period='max')
    tz_df = df.iloc[0].name.tz
    timestamp = pd.Timestamp.today(tz=tz_df) - pd.DateOffset(months=months)
    return df[df.index > timestamp]


def get_last_days(days: int, company: str) -> pd.core.frame.DataFrame :
    df = get_comp_stock_hist(company=company, period='max')
    tz_df = df.iloc[0].name.tz
    timestamp = pd.Timestamp.today(tz=tz_df) - pd.DateOffset(days=days)
    return df[df.index > timestamp]
