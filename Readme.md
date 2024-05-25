# StockView
Welcome to my little Python project called StockView.
With Stockview, you can plot common stock indicators for stocks.
Additionally, you can easily customize the parameters of the indicators.
The following indicators are already implemented:

1. **Moving average indicators:**
    - Simple Moving Average (SMA)
    - Exponential Moving Average (EMA)
    - Weighted Moving Average (WMA)

1. **Trend indicators:**
    - Average Directional Index (ADX)
    - Moving Average Convergence/Divergence (MACD)

1. **Price Channels:** 
    - Bollinger Bands
    - Donchian Channel


----
## Getting started
The repository has been tested on Ubuntu 20.04 with Python 3.9.5.
It is recommended to use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The script [`stockview.py`](stockview.py) contains an example of all indicators for the company VW.
```bash
python stockview.py
```

![](docs/MovingAverageIndicators_VW.png?raw=true)
![](docs/ADX14_VW.png?raw=true)
![](docs/MACD12-26_VW.png?raw=true)
![](docs/BollingerBands_VW.png?raw=true)
![](docs/DonchianChannel_VW.png?raw=true)
