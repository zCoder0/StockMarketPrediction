from src.exception.exception import ProjectException
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from src.Model.model import Model  # Assuming Model class is in src/model.py

    # Run the prediction loop

try:
        
    # Streamlit UI Setup
    st.title("Stock Price Prediction using ARIMA")

    # User Input: Stock Ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")

    # Placeholder for live updating graph
    chart_placeholder = st.empty()

    # Button to Start Prediction
    if st.button("Start Live Prediction"):
        model_instance = Model()
        while True:
            data = model_instance.get_stock_data(ticker)
            if data is not None:
                model_fit, data_series = model_instance.train_arima_model(data)
                next_price = model_instance.predict_next_hour(model_fit)
                
                st.write(f"### Predicted Next Hour Price: **${next_price[0]}**")
                
                # Plot
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(data.index, data['Close'], label="Actual Prices", color="blue", marker="o")
                next_time = data.index[-1] + pd.Timedelta(hours=1)
                ax.scatter(next_time, next_price, color="red", label="Predicted Price", marker="x", s=100)
                ax.set_xlabel("Time")
                ax.set_ylabel("Stock Price ($)")
                ax.set_title("Stock Price Prediction (Next 1 Hour)")
                ax.legend()
                
                chart_placeholder.pyplot(fig)
                time.sleep(60)  # Update every 60 seconds
            else:
                st.error("Failed to fetch stock data. Please try again!")
                break

except Exception as e:
    print(e)
    ProjectException(e,sys)
