# Financial Analysis Tool - ACC102 Track4
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 页面设置
st.set_page_config(page_title="Stock Analyzer", page_icon="📈")
st.title("📊 Stock Financial Analysis Tool")
st.caption("ACC102 Data Product | XJTLU")

# 输入
ticker = st.text_input("Stock Ticker (e.g. AAPL, MSFT, AMZN)", "AAPL")
period = st.selectbox("Time Period", ["1y", "6mo", "3mo", "1mo"])

# 分析按钮
if st.button("Start Analysis"):
    with st.spinner("Fetching data..."):
        # 获取数据
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty:
            st.error("Invalid ticker or no data!")
        else:
            # 数据清洗
            df = df.dropna()
            df["Daily Return"] = df["Close"].pct_change()

            # 计算指标
            latest_close = round(df["Close"].iloc[-1], 2)
            cum_return = round((df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100, 2)
            volatility = round(df["Daily Return"].std() * np.sqrt(252) * 100, 2)

            # 展示结果
            st.subheader(f"Analysis Result: {ticker}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Latest Close", f"${latest_close}")
            col2.metric("Total Return", f"{cum_return}%")
            col3.metric("Annual Volatility", f"{volatility}%")

            # 图表
            st.subheader("Price Trend")
            st.line_chart(df["Close"], color="#0066cc")

            st.success("Analysis completed!")