import discord
from discord import app_commands
import aiohttp

sad_words = [
    "sad", "depressed", "alone", "lonely", "hopeless", "worthless", "tired",
    "empty", "broken", "hurt", "lost", "anxious", "afraid", "miserable",
    "crying", "stressed", "regret", "failure", "despair", "ashamed",
    "abandoned", "pain", "fear", "grief", "insecure", "unloved", "stupid", "dumb",
]

# Event that response sad words
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if any(word in message.content.lower() for word in sad_words):
        await message.reply("Don't feel down — you will get through this.")

# Get a inspirational quote to send (API zenquotes)        
async def get_inspirational_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zenquotes.io/api/random') as resp:
            data = await resp.json()
            quote_data = data[0]
            quote = quote_data.get("q", "No quote found")
            author = quote_data.get("a") or "Unknown"
            return f"{quote} - {author}"

# Function that register the commands
def register_quotes(tree: app_commands.CommandTree):
    # Send inspirational quotes
    @tree.command(name='inspiration', description='Send a random inspirational quote')
    async def inspiration(interaction: discord.Interaction):
        await interaction.response.defer()

        quote = await get_inspirational_quote()
        await interaction.followup.send(quote)