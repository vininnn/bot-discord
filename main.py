import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime, timezone
import os

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

# Bot initialization
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'Synchro: {len(synced)}')
    print('All right!')

activity = {}

@bot.tree.command(name='start_studying', description='Start a timer for a specific study subject')
@app_commands.describe(text='Study subject')
async def start_studying(interaction: discord.Interaction, studySubject: str):
    activity[studySubject] = datetime.now(timezone.utc)
    await interaction.response.send_message(f'Timer was successfully! Study subject: {studySubject}')

@bot.tree.command(name='finish_studying', description='Finish a timer for a specific study subject already initialized')
@app_commands.describe(text='Finish subject')
async def start_studying(interaction: discord.Interaction, studySubject: str):
    if activity is None:
        await interaction.response.send_message(f'There are no timers to finish!')
        return
    try:
        studyDuration = activity.pop[studySubject]
        await interaction.response.send_message(f'Timer was finished successfully! Time studying {studySubject}: {studyDuration}')
    except:
        await interaction.response.send_message(f'There are no timers named {studySubject}!')


bot.run(os.getenv('TOKEN'))