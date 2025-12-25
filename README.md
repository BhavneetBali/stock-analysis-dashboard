# Stock Analysis Web App

A Python-based equity analysis dashboard that computes risk-adjusted
performance metrics and visualizes stock price behavior.

## Features
- Live market data using yfinance
- CAGR, Volatility, Sharpe Ratio, Max Drawdown
- Interactive web interface using Streamlit
- Supports MultiIndex price data

## Tech Stack
- Python
- pandas, numpy
- Streamlit
- yfinance

## How to Run
From inside `stock_analysis_app/`:

```bash
pip install -r requirements.txt
streamlit run app.py

## Motivation
This project follows a research-to-production workflow:
financial logic was validated in Jupyter notebooks before
being modularized and deployed as a Python web application.

