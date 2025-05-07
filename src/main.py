import asyncio
import datetime
from src.data.data_fetcher import DataFetcher
from src.models.lstm_model import LSTMModel
from src.bots.telegram_bot import TelegramBot
from src.bots.discord_bot import DiscordBot
from src.utils.config import Config
from src.utils.logger import setup_logger
import numpy as np
from sklearn.preprocessing import MinMaxScaler

async def main():
    logger = setup_logger(__name__)
    logger.info("Starting stock prediction bot")

    # Initialize components
    data_fetcher = DataFetcher(Config.STOCK_SYMBOL)
    lstm_model = LSTMModel(Config.PREDICTION_DAYS)
    telegram_bot = TelegramBot()
    discord_bot = DiscordBot()

    try:
        # Fetch and preprocess data
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        df = data_fetcher.fetch_data(start_date, end_date)
        X_train, y_train, X_test, y_test, scaled_data = data_fetcher.preprocess_data(df, Config.PREDICTION_DAYS)

        # Build and train model
        lstm_model.build_model()
        lstm_model.train(X_train, y_train)

        # Evaluate model
        loss = lstm_model.evaluate(X_test, y_test)
        logger.info(f"Model evaluation loss: {loss}")

        # Make prediction for the next day
        last_sequence = scaled_data[-Config.PREDICTION_DAYS:]
        last_sequence = np.reshape(last_sequence, (1, Config.PREDICTION_DAYS, 1))
        predicted_scaled = lstm_model.predict(last_sequence)
        predicted_price = data_fetcher.scaler.inverse_transform(predicted_scaled)[0][0]

        # Format prediction message
        prediction_message = f"Predicted {Config.STOCK_SYMBOL} price for tomorrow: ${predicted_price:.2f}"

        # Start bots and send predictions
        tasks = [
            telegram_bot.start(),
            discord_bot.start(),
            telegram_bot.send_prediction(prediction_message),
            discord_bot.send_prediction(prediction_message)
        ]
        await asyncio.gather(*tasks)

    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
