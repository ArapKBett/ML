import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from src.utils.logger import setup_logger

class DataFetcher:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.logger = setup_logger(__name__)
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def fetch_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        self.logger.info(f"Fetching data for {self.symbol} from {start_date} to {end_date}")
        try:
            stock = yf.Ticker(self.symbol)
            df = stock.history(start=start_date, end=end_date)
            if df.empty:
                raise ValueError("No data retrieved")
            return df[['Close']]
        except Exception as e:
            self.logger.error(f"Error fetching data: {e}")
            raise

    def preprocess_data(self, df: pd.DataFrame, look_back: int) -> tuple:
        self.logger.info("Preprocessing data")
        try:
            # Scale the data
            scaled_data = self.scaler.fit_transform(df.values)
            
            # Create sequences for LSTM
            X, y = [], []
            for i in range(look_back, len(scaled_data)):
                X.append(scaled_data[i-look_back:i, 0])
                y.append(scaled_data[i, 0])
            
            X, y = np.array(X), np.array(y)
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))
            
            # Split into train and test
            train_size = int(len(X) * 0.8)
            X_train, X_test = X[:train_size], X[train_size:]
            y_train, y_test = y[:train_size], y[train_size:]
            
            return X_train, y_train, X_test, y_test, scaled_data
        except Exception as e:
            self.logger.error(f"Error preprocessing data: {e}")
            raise
