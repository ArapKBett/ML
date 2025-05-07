import discord
from discord.ext import commands
from src.utils.config import Config
from src.utils.logger import setup_logger

class DiscordBot:
    def __init__(self):
        self.token = Config.DISCORD_TOKEN
        self.channel_id = int(Config.DISCORD_CHANNEL_ID)
        self.logger = setup_logger(__name__)
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='/', intents=intents)

    async def start(self):
        self.logger.info("Starting Discord bot")
        try:
            @self.bot.event
            async def on_ready():
                self.logger.info(f"Discord bot logged in as {self.bot.user}")

            @self.bot.command(name='predict')
            async def predict_command(ctx):
                self.logger.info("Received /predict command")
                try:
                    await ctx.send("Predicting stock price...")
                    # Placeholder for prediction logic
                    prediction = "Sample prediction: $150.25"  # Replace with actual prediction
                    channel = self.bot.get_channel(self.channel_id)
                    await channel.send(prediction)
                except Exception as e:
                    self.logger.error(f"Error in predict command: {e}")
                    await ctx.send("Error making prediction")

            await self.bot.start(self.token)
        except Exception as e:
            self.logger.error(f"Error starting Discord bot: {e}")
            raise

    async def send_prediction(self, prediction: str):
        self.logger.info(f"Sending prediction to Discord channel: {prediction}")
        try:
            channel = self.bot.get_channel(self.channel_id)
            await channel.send(prediction)
        except Exception as e:
            self.logger.error(f"Error sending Discord message: {e}")
            raise
