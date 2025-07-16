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

study_sessions = {}

# Format the study duration (HH:MM:SS)
def format_study_duration(study_duration):
    total_seconds = int(study_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f'{hours:02}:{minutes:02}:{seconds:02}' 

# Start a study session
@bot.tree.command(name='start_studying', description='Start a timer for a specific study subject')
@app_commands.describe(topic='Study subject')
async def start_studying(interaction: discord.Interaction, topic: str):
    await interaction.response.defer()

    if topic in study_sessions:
        await interaction.followup.send(f'There is already a session named "{topic}" in progress!')
        return

    study_sessions[topic] = datetime.now(timezone.utc)
    await interaction.followup.send(f'Timer started successfully! Study subject: "{topic}"')

# End a study session
@bot.tree.command(name='finish_studying', description='Finish a timer for a specific study subject already initialized')
@app_commands.describe(topic='Finish subject')
async def finish_studying(interaction: discord.Interaction, topic: str):
    await interaction.response.defer()

    if topic not in study_sessions:
        await interaction.followup.send(f'There are no timers named "{topic}"!')
        return

    start_time = study_sessions.pop(topic)
    study_duration = datetime.now(timezone.utc) - start_time
    formatted_study_duration = format_study_duration(study_duration)
    await interaction.followup.send(f'Timer finished successfully! Time spent on "{topic}":  {formatted_study_duration}')


bot.run(os.getenv('TOKEN'))