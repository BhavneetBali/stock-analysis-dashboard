import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

from finance_utils import compute_metrics

st.set_page_config(page_title="Stock Analysis App", layout="centered")

st.title("Stock Analysis Dashboard")
st.write("Simple equity performance and risk analysis")

TICKERS = {
    "India": {
        "RELIANCE.NS": "Reliance Industries",
        "TCS.NS": "Tata Consultancy Services",
        "INFY.NS": "Infosys",
        "HDFCBANK.NS": "HDFC Bank",
        "ICICIBANK.NS": "ICICI Bank"
    },
    "US": {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet",
        "AMZN": "Amazon",
        "NVDA": "NVIDIA"
    }
}

# Input
region = st.selectbox("Market", list(TICKERS.keys()))

ticker = st.selectbox(
    "Select Stock (type to search)",
    options=list(TICKERS[region].keys()),
    format_func=lambda x: f"{x} — {TICKERS[region][x]}"
)

period = st.selectbox("Select Time Period", ["1y", "3y", "5y"])
risk_free_rate_pct = st.number_input(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=15.0,
    value=6.0,
    step=0.5
)

risk_free_rate = risk_free_rate_pct / 100


BENCHMARKS = {
    "India": "^NSEI",     # NIFTY 50
    "US": "^GSPC"        # S&P 500
}

benchmark_ticker = BENCHMARKS[region]

benchmark_data = yf.download(benchmark_ticker, period=period)

if isinstance(benchmark_data.columns, pd.MultiIndex):
    benchmark_prices = benchmark_data[("Close", benchmark_ticker)]
else:
    benchmark_prices = benchmark_data["Close"]

benchmark_prices = benchmark_prices.dropna()

benchmark_returns = benchmark_prices.pct_change().dropna()

benchmark_cagr = (
    benchmark_prices.iloc[-1] /
    benchmark_prices.iloc[0]
) ** (252 / len(benchmark_returns)) - 1

benchmark_cagr = float(benchmark_cagr)


# Streamlit Dashboarding
if st.button("Run Analysis"):
    with st.spinner("Fetching data..."):
        data = yf.download(ticker, period=period)

    if data.empty:
        st.error("Invalid ticker or no data available.")
    else:
        prices, metrics, drawdown = compute_metrics(
            data, ticker, risk_free_rate
        )

        # --- Price Chart ---
        st.subheader("Price Chart")
        st.line_chart(prices)

        # --- Metrics ---
        st.subheader("Key Metrics")
        cols = st.columns(4)
        for col, (k, v) in zip(cols, metrics.items()):
            col.metric(k, v)

        st.subheader("Stock vs Benchmark")
        col1, col2 = st.columns(2)
        col1.metric(
            "Stock CAGR (%)",
            round(metrics["CAGR (%)"], 2)
        )
        col2.metric(
            "Benchmark CAGR (%)",
            round(benchmark_cagr * 100, 2)
        )

        excess_return = metrics["CAGR (%)"] - (benchmark_cagr * 100)
        st.caption(
            f"Excess return over benchmark: {excess_return:.2f}%"
        )


        # --- Drawdown Chart ---
        st.subheader("Drawdown Analysis")
        drawdown_df = drawdown.to_frame(name="Drawdown")
        st.line_chart(drawdown_df)
        with st.expander("Advanced Risk View"):
        # matplotlib drawdown with annotations
            st.subheader("Drawdown Analysis")

            fig, ax = plt.subplots(figsize=(10, 4))
            
            ax.fill_between(
                drawdown.index,
                drawdown,
                0,
                color="red",
                alpha=0.25,
                label="Drawdown"
            )
            
            # Highlight max drawdown
            max_dd_date = drawdown.idxmin()
            max_dd_value = drawdown.min()
            
            ax.scatter(
                max_dd_date,
                max_dd_value,
                color="darkred",
                zorder=5
            )
            
            ax.annotate(
                f"Max DD: {max_dd_value:.1%}",
                xy=(max_dd_date, max_dd_value),
                xytext=(max_dd_date, max_dd_value * 0.5),
                arrowprops=dict(arrowstyle="->", color="darkred"),
                fontsize=9
            )
            
            ax.set_title("Drawdown from Peak", fontsize=12)
            ax.set_ylabel("Drawdown (%)")
            ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
            
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.grid(axis="y", alpha=0.3)
            
            st.pyplot(fig)

        
        #Stock VS Benchmark
        normalized_stock = prices / prices.iloc[0] * 100
        normalized_benchmark = benchmark_prices / benchmark_prices.iloc[0] * 100

        st.subheader("Relative Performance (Normalized to 100)")
        comparison_df = pd.DataFrame({
            ticker: normalized_stock,
            benchmark_ticker: normalized_benchmark
        })

        st.line_chart(comparison_df)

        
        
                
