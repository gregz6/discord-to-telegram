import discord
import asyncio
from telegram import Bot
import os

# Patch discord.gateway.WSClient.received_message to fix the pending_payments issue
import discord.gateway

old_received_message = discord.gateway.WSClient.received_message

async def patched_received_message(self, data):
    # If 'pending_payments' is None, change it to an empty list
    if isinstance(data, dict) and 'pending_payments' in data and data['pending_payments'] is None:
        data['pending_payments'] = []
    return await old_received_message(self, data)

discord.gateway.WSClient.received_message = patched_received_message

# Load environment variables
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

# Initialize the Telegram bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def on_message(self, message):
        try:
            # Only process messages from the target channel and ignore your own messages
            if message.channel.id != DISCORD_CHANNEL_ID or message.author.id == self.user.id:
                return

            # Forward text messages
            if message.content:
                msg = f"[{message.author.display_name}] {message.content}"
                await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

            # Safely iterate through attachments even if it's None
            for attachment in (message.attachments or []):
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=attachment.url)
        except Exception as e:
            # Log any errors during message processing to avoid crashing
            print(f"Error processing message: {e}")

client = MyClient()
client.run(DISCORD_TOKEN)
