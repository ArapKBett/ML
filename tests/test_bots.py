import pytest
import asyncio
from src.bots.telegram_bot import TelegramBot
from src.bots.discord_bot import DiscordBot

@pytest.mark.asyncio
async def test_telegram_send_prediction(monkeypatch):
    async def mock_send_message(*args, **kwargs):
        return True

    monkeypatch.setattr("telegram.Bot.send_message", mock_send_message)
    telegram_bot = TelegramBot()
    await telegram_bot.send_prediction("Test prediction")
    assert True  # If no exception, test passes

@pytest.mark.asyncio
async def test_discord_send_prediction(monkeypatch):
    async def mock_send(*args, **kwargs):
        return True

    monkeypatch.setattr("discord.abc.Messageable.send", mock_send)
    discord_bot = DiscordBot()
    await discord_bot.send_prediction("Test prediction")
    assert True  # If no exception, test passes
