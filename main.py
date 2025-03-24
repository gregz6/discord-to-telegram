import discord
import asyncio
from telegram import Bot
import os

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def on_message(self, message):
        if message.channel.id != DISCORD_CHANNEL_ID:
            return

        if message.author.id == self.user.id:
            return

        if message.content:
            msg = f"[{message.author.display_name}] {message.content}"
            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=attachment.url)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN, bot=False)  # <<< IMPORTANT for self-bot
