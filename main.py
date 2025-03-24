import discord
from telegram import Bot
import os

# Load environment variables
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Set up multiple channel IDs from a comma-separated string
DISCORD_CHANNEL_IDS = os.environ["DISCORD_CHANNEL_IDS"].split(',')
DISCORD_CHANNEL_IDS = [int(cid.strip()) for cid in DISCORD_CHANNEL_IDS]

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

# Initialize the Telegram bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        # Send a test message to Telegram to confirm the bot is online
        await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Test message: Bot is online!")

    async def on_message(self, message):
        # Process messages only if they come from one of the target channels
        # and ignore messages sent by yourself
        if message.channel.id not in DISCORD_CHANNEL_IDS or message.author.id == self.user.id:
            return

        # Forward text messages
        if message.content:
            msg = f"[{message.author.display_name}] {message.content}"
            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

        # Forward image attachments
        for attachment in (message.attachments or []):
            if attachment.content_type and attachment.content_type.startswith("image/"):
                await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=attachment.url)

client = MyClient()
client.run(DISCORD_TOKEN)
