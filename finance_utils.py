import numpy as np
import pandas as pd

def extract_close_price(df, ticker):
    if isinstance(df.columns, pd.MultiIndex):
        return df[('Close', ticker)].rename("Close")
    else:
        return df['Close']

def compute_metrics(df, ticker, rf=0.06):
    prices = extract_close_price(df, ticker)
    returns = prices.pct_change().dropna()

    cagr = (prices.iloc[-1] / prices.iloc[0]) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe = (cagr - rf) / volatility

    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns / rolling_max) - 1

    # ---- Drawdown Duration ----
    is_underwater = drawdown < 0
    drawdown_duration = is_underwater.astype(int).groupby(
        (~is_underwater).cumsum()
    ).cumsum()
    max_dd_duration = drawdown_duration.max()

    metrics = {
        "CAGR (%)": round(cagr * 100, 2),
        "Volatility (%)": round(volatility * 100, 2),
        "Sharpe Ratio": round(sharpe, 2),
        "Max Drawdown (%)": round(drawdown.min() * 100, 2),
        "Max DD Duration (days)": int(max_dd_duration)
    }

    return prices, metrics, drawdown


