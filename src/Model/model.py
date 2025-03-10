from src.exception.exception import ProjectException
import sys
import yfinance as yf
import pandas as pd
import time
from statsmodels.tsa.arima.model import ARIMA
import warnings
import numpy as np
import os
warnings.filterwarnings("ignore")  # Ignore ARIMA warnings
import matplotlib.pyplot as plt
from src.logging import logger
class Model:
    def __init__(self):
        self.path = 'src/data/'
        os.makedirs(self.path ,exist_ok=True)
        
    def get_stock_data(self,ticker):
        try:
            self.ticker = ticker
            stock = yf.Ticker(ticker)
            data = stock.history(period="1y", interval="1d")  # 1-month hourly data
            pd.DataFrame(data).to_csv(os.path.join(self.path,"data_series.csv"))
            data = data[['Close']].dropna()  # Keep only 'Close' prices
            data.index = data.index.tz_localize(None)  # Remove timezone info
            return data
            
        except Exception as e:
            print(f"An error occurred: {e}")
            ProjectException(e,sys)
    
        
    # Automatically Find Best (p,d,q) for ARIMA
    def auto_arima_order(self,data):
        best_aic = np.inf
        best_order = None

        for p in range(0, 3):  # Try p from 0 to 2
            for d in range(0, 2):  # Try d from 0 to 1
                for q in range(0, 3):  # Try q from 0 to 2
                    try:
                        model = ARIMA(data, order=(p, d, q))
                        result = model.fit()
                        if result.aic < best_aic:
                            best_aic = result.aic
                            best_order = (p, d, q)
                    except:
                        continue
        return best_order if best_order else (2, 1, 2)  # Default if no optimal order is found

    
    # Train ARIMA Model
    def train_arima_model(self,data):
        try:
            data_series = data['Close'].reset_index(drop=True)  # Convert to Series
            best_order = self.auto_arima_order(data_series)
            print(f"Using ARIMA Order: {best_order}")  # Debugging Info
            model = ARIMA(data_series, order=best_order)
            model_fit = model.fit()

            return model_fit , data_series
        except Exception as e:
            print(f"An error occurred: {e}")
            ProjectException(e,sys)
            
    # Predict Next 1-Hour Price
    def predict_next_hour(self,model):
        try:
            forecast = model.forecast(steps=1)  # Get single prediction
            forecast = forecast.tolist()
            forecast = [round(num, 2) for num in forecast]   # Round to 2 decimal places
            logger.logging.info(f"Predicted Next Hour Price : {forecast[0]}  Ticker Name : ({self.ticker})")  # Log prediction
            return forecast
        except Exception as e:
                print(f"An error occurred: {e}")
                ProjectException(e,sys)
                
    # Plot Stock Prices & Prediction
    def plot_stock_prediction(self,data, prediction):
        try:
            plt.figure(figsize=(20, 10))
            plt.plot(data.index, data['Close'], label="Actual Prices", color="blue", marker="o")
            
            # Add predicted next price (extend the index)
            next_time = data.index[-1] + pd.Timedelta(hours=1)  # Next 1-hour time
            plt.scatter(next_time, prediction, color="red", label="Predicted Price", marker="x", s=100)
            
            plt.xlabel("Time")
            plt.ylabel("Stock Price ($)")
            plt.title("Stock Price Prediction (Next 1 Hour)")
            plt.legend()
            plt.grid(True)
            plt.show()
        except Exception as e:
            print(f"An error occurred: {e}")
            ProjectException(e,sys)
              
    
        # Continuous Prediction Every Hour
    def run_prediction(self, ticker):
        try:
            print(f"Starting Stock Price Prediction for: {ticker}")
            
            for _ in range(24):  # Run for 24 hours
                try:
                    print("\nFetching latest data...")
                    data = self.get_stock_data(ticker)
                    model, data_series = self.train_arima_model(data)
                    next_price = self.predict_next_hour(model)
                    
                    print(f"Predicted Next Price: ${next_price}")
                    self.plot_stock_prediction(data, next_price)  # Plot actual & predicted values
                except Exception as e:
                    print(f"Error: {e}")
                
                print("Waiting for the next prediction (1 minute)...")
                time.sleep(60)  # Sleep for 1 hour before the next prediction
        except Exception as e:
            print(f"An error occurred: {e}")
            ProjectException(e,sys)
              