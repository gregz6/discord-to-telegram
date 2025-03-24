import discord
import asyncio
from telegram import Bot
import os

# --- Patch for pending_payments issue (if needed) ---
import discord.state

original_parse_ready_supplemental = discord.state.ConnectionState.parse_ready_supplemental

def patched_parse_ready_supplemental(self, data):
    if data.get("pending_payments") is None:
        data["pending_payments"] = []
    try:
        return original_parse_ready_supplemental(self, data)
    except TypeError as e:
        print("Caught TypeError in parse_ready_supplemental:", e)
        self.pending_payments = {}
        return None

discord.state.ConnectionState.parse_ready_supplemental = patched_parse_ready_supplemental
# --- End Patch ---

# Load environment variables
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
# Instead of a single channel, use a comma-separated list of channel IDs:
DISCORD_CHANNEL_IDS = os.environ["DISCORD_CHANNEL_IDS"].split(',')
# Convert them to integers (strip spaces in case)
DISCORD_CHANNEL_IDS = [int(cid.strip()) for cid in DISCORD_CHANNEL_IDS]

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

# Initialize the Telegram bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def on_message(self, message):
        try:
            # Process only messages from the target channels and ignore your own messages
            if message.channel.id not in DISCORD_CHANNEL_IDS or message.author.id == self.user.id:
                return

            # Forward text messages
            if message.content:
                msg = f"[{message.author.display_name}] {message.content}"
                await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

            # Safely iterate through attachments
            for attachment in (message.attachments or []):
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=attachment.url)
        except Exception as e:
            print(f"Error processing message: {e}")

client = MyClient()
client.run(DISCORD_TOKEN)
