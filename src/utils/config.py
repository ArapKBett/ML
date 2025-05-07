from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
    STOCK_SYMBOL = "AAPL"  # Default stock symbol
    PREDICTION_DAYS = 60  # Look-back period for LSTM
    FUTURE_DAYS = 1  # Predict next day
