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
        # Check if message is from one of the target channels and ignore your own messages
        if message.channel.id not in DISCORD_CHANNEL_IDS or message.author.id == self.user.id:
            return

        # Forward text messages
        if message.content:
            msg = f"[{message.author.display_name}] {message.content}"
            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

        # Loop through attachments and print debug info
        for attachment in (message.attachments or []):
            # Print debug information to your logs
            print(f"DEBUG: attachment filename={attachment.filename}, content_type={attachment.content_type}")

            # If the attachment is labeled as an image, send as a photo
            if attachment.content_type and "image" in attachment.content_type:
                await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=attachment.url)
            else:
                # Otherwise, send it as a document (fallback)
                await telegram_bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=attachment.url)

client = MyClient()
client.run(DISCORD_TOKEN)
