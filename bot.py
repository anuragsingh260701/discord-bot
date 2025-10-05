import discord
from deep_translator import GoogleTranslator
from langdetect import detect
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Only respond if the bot is mentioned
    if client.user in message.mentions:
        orig_text = message.content.replace(f"<@{client.user.id}>", "").strip()

        if not orig_text:
            await message.channel.send("Please provide text to translate.")
            return

        try:
            # Auto-detect language and translate accordingly
            lang = detect(orig_text)
            if lang == 'ja':
                translated = GoogleTranslator(source='ja', target='en').translate(orig_text)
                await message.channel.send(f"Japanese ➔ English: {translated}")
            else:
                translated = GoogleTranslator(source='en', target='ja').translate(orig_text)
                await message.channel.send(f"English ➔ Japanese: [translate:{translated}]")
        except Exception as e:
            await message.channel.send("Translation failed, please try again later.")
            print(f"Translation error: {e}")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
print(f"TOKEN: {TOKEN}")
client.run(TOKEN)
