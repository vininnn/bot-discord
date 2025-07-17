import discord
from discord import app_commands
from datetime import datetime, timezone

study_sessions = {}
ended_sessions = {}

# Format the study duration (HH:MM:SS)
def format_study_duration(study_duration):
    total_seconds = int(study_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f'{hours:02}:{minutes:02}:{seconds:02}' 

# Function that register the commands
def register_study_sessions(tree: app_commands.CommandTree):
    # Start a study session
    @tree.command(name='start', description='Start a timer for a specific study subject')
    @app_commands.describe(subject='Study subject')
    async def start(interaction: discord.Interaction, subject: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        
        if user_id in study_sessions:
            await interaction.followup.send(f'You are already in a study session! Quit it before you join another!')
            return

        study_sessions[user_id] = {subject: datetime.now(timezone.utc)}

        await interaction.followup.send(f'Timer started successfully! Study subject: "{subject}"')

    # End a study session
    @tree.command(name='finish', description='Finish a timer for a specific study subject already initialized')
    @app_commands.describe(subject='Finish subject')
    async def finish(interaction: discord.Interaction, subject: str):
        await interaction.response.defer()

        user_id = interaction.user.id

        if user_id not in study_sessions:
            await interaction.followup.send(f'You are not in a study session yet! Join one!')
            return

        if subject not in study_sessions[user_id]:
            await interaction.followup.send(f'There are no timers named "{subject}"!')
            return

        start_time = study_sessions[user_id].pop(subject)
        study_duration = datetime.now(timezone.utc) - start_time

        if user_id not in ended_sessions:
            ended_sessions[user_id] = {}

        if subject not in ended_sessions[user_id]:
            ended_sessions[user_id][subject] = study_duration
        else:
            ended_sessions[user_id][subject] += study_duration

        formatted_study_duration = format_study_duration(study_duration)
        await interaction.followup.send(f'Timer finished successfully! Time spent on "{subject}":  {formatted_study_duration}')

    # Shows the total time per subject
    @tree.command(name='summary', description='Shows the total hours studied in the subject')
    @app_commands.describe(subject='Total time on subject')
    async def summary(interaction: discord.Interaction, subject: str):
        await interaction.response.defer()

        user_id = interaction.user.id

        if user_id not in ended_sessions:
            await interaction.followup.send(f'You have no ended sessions!')
            return

        if subject not in ended_sessions[user_id]:
            await interaction.followup.send(f'There are no ended sessions named "{subject}"!')
            return

        formatted_time = format_study_duration(ended_sessions[user_id][subject])
        await interaction.followup.send(f'Time spent on "{subject}":  {formatted_time}')    
