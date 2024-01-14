# Welcome to StockView

With Stockview, you can plot common stock indicators for any stocks.
Additionally, you can easily customize the parameters of the indicators.
The following indicators are already implemented:

1. **Moving average indicators:**
- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Weighted Moving Average (WMA)

2. **Trend indicators:**
- Average Directional Index (ADX)
- Moving Average Convergence/Divergence (MACD)


----
## Build & Installation
The repository has been tested on Ubuntu 20.04 with Python 3.9.5.
It is recommended to use a virtual environment:
```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```


----
## Getting started
The script [`stockview.py`](stockview.py) contains an example of all indicators for the company VW.
```bash
    python stockview.py
```

![](docs/MovingAverageIndicators_VW.png?raw=true)
![](docs/ADX14_VW.png?raw=true)
![](docs/MACD12-26_VW.png?raw=true)
