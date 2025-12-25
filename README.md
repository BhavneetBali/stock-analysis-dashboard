# Stock Analysis Dashboard

A Python-based equity analysis web application that evaluates stock
performance relative to market benchmarks using risk-adjusted metrics.

## Features
- Stock selection with autocomplete dropdown
- Benchmark comparison (NIFTY 50 / S&P 500)
- CAGR, Volatility, Sharpe Ratio
- Max Drawdown and Drawdown Duration
- Normalized stock vs benchmark performance
- Clean dashboard + advanced risk view

## Methodology
This project follows a **research-to-production workflow**:
financial logic was first validated in Jupyter notebooks and then
modularized into a production-ready Streamlit application.

## Tech Stack
- Python
- pandas, numpy
- yfinance
- Streamlit
- matplotlib

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Motivation
Built to demonstrate financial intuition, downside risk analysis,
and clean analytics-to-product design.

