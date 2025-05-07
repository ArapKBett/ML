from telegram import Bot
from telegram.ext import Application, CommandHandler
from src.utils.config import Config
from src.utils.logger import setup_logger
import asyncio

class TelegramBot:
    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        self.channel_id = Config.TELEGRAM_CHANNEL_ID
        self.logger = setup_logger(__name__)
        self.bot = Bot(token=self.token)
        self.app = Application.builder().token(self.token).build()

    async def start(self):
        self.logger.info("Starting Telegram bot")
        self.app.add_handler(CommandHandler("predict", self.predict_command))
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def predict_command(self, update, context):
        self.logger.info("Received /predict command")
        try:
            await update.message.reply_text("Predicting stock price...")
            # Placeholder for prediction logic
            prediction = "Sample prediction: $150.25"  # Replace with actual prediction
            await self.bot.send_message(chat_id=self.channel_id, text=prediction)
        except Exception as e:
            self.logger.error(f"Error in predict command: {e}")
            await update.message.reply_text("Error making prediction")

    async def send_prediction(self, prediction: str):
        self.logger.info(f"Sending prediction to Telegram channel: {prediction}")
        try:
            await self.bot.send_message(chat_id=self.channel_id, text=prediction)
        except Exception as e:
            self.logger.error(f"Error sending Telegram message: {e}")
            raise
