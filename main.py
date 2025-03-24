import discord
import asyncio
from telegram import Bot
import os

# Patch the ConnectionState.parse_ready_supplemental method in discord.state
import discord.state

original_parse_ready_supplemental = discord.state.ConnectionState.parse_ready_supplemental

def patched_parse_ready_supplemental(self, data):
    # Ensure pending_payments is a list, even if it comes in as None
    if data.get("pending_payments") is None:
        data["pending_payments"] = []
    try:
        return original_parse_ready_supplemental(self, data)
    except TypeError as e:
        # Catch the error and bypass the payments processing
        print("Caught TypeError in parse_ready_supplemental:", e)
        self.pending_payments = {}
        return None

discord.state.ConnectionState.parse_ready_supplemental = patched_parse_ready_supplemental

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
