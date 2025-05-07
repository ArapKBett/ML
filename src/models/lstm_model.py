import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from src.utils.logger import setup_logger
import numpy as np

class LSTMModel:
    def __init__(self, look_back: int):
        self.look_back = look_back
        self.model = None
        self.logger = setup_logger(__name__)

    def build_model(self):
        self.logger.info("Building LSTM model")
        try:
            self.model = Sequential()
            self.model.add(LSTM(units=50, return_sequences=True, input_shape=(self.look_back, 1)))
            self.model.add(Dropout(0.2))
            self.model.add(LSTM(units=50, return_sequences=False))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(units=25))
            self.model.add(Dense(units=1))
            self.model.compile(optimizer='adam', loss='mean_squared_error')
        except Exception as e:
            self.logger.error(f"Error building model: {e}")
            raise

    def train(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 50, batch_size: int = 32):
        self.logger.info("Training LSTM model")
        try:
            self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
        except Exception as e:
            self.logger.error(f"Error training model: {e}")
            raise

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        self.logger.info("Making predictions")
        try:
            return self.model.predict(X_test)
        except Exception as e:
            self.logger.error(f"Error predicting: {e}")
            raise

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        self.logger.info("Evaluating model")
        try:
            return self.model.evaluate(X_test, y_test)
        except Exception as e:
            self.logger.error(f"Error evaluating model: {e}")
            raise
