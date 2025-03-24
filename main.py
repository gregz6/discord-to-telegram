import discord
import asyncio
from telegram import Bot
import os

# --- CONFIG SECTION ---
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])
# ----------------------

# Telegram bot setup
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Discord client setup (no intents needed)
class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

      async def on_message(self, message):
        if message.channel.id != DISCORD_CHANNEL_ID:
            return

        if message.author.id == self.user.id:
            return

        # Send the text message (if there is any)
        if message.content:
            msg = f"[{message.author.display_name}] {message.content}"
            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

        # Send image attachments (if any)
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=attachment.url)

# Create and run client
client = MyClient()
client.run(DISCORD_TOKEN)
