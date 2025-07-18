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
    @tree.command(name='startstudy', description='Start a timer for a specific study subject')
    @app_commands.describe(subject='Study subject')
    async def startstudy(interaction: discord.Interaction, subject: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        
        if user_id in study_sessions:
            await interaction.followup.send('You are already in a study session! Quit it before you join another!')
            return

        study_sessions[user_id] = {subject: datetime.now(timezone.utc)}

        await interaction.followup.send(f'Timer started successfully! Study subject: "{subject}"')
    
    # Start a study session in a group
    @tree.command(name='startwith', description='Start a timer for a specific study subject to study in a group')
    @app_commands.describe(subject='Study subject', partner1='Who will study with you?', partner2='Who will study with you?', partner3='Who will study with you?', partner4='Who will study with you?', partner5='Who will study with you?')
    async def startwith(
        interaction: discord.Interaction,
        subject: str,
        partner1: discord.Member,
        partner2: discord.Member = None,
        partner3: discord.Member = None,
        partner4: discord.Member = None,
        partner5: discord.Member = None,
        ):
        await interaction.response.defer()

        user_id = interaction.user.id
        if user_id in study_sessions:
            await interaction.followup.send('You are already in a study session! Quit it before you join another!')
            return
        
        partners = []
        unvalidated_partner = [partner1]
        if partner2:
            unvalidated_partner.append(partner2)
        if partner3:
            unvalidated_partner.append(partner3)
        if partner4:
            unvalidated_partner.append(partner4)
        if partner5:
            unvalidated_partner.append(partner5)
            
        for partner in unvalidated_partner:
            if partner.bot:
                await interaction.followup.send('You cannot add a bot as a study partner')
                return
            elif partner.id == user_id:
                await interaction.followup.send('You cannot add yourself as a study partner')
                return
            elif partner.id in study_sessions:
                await interaction.followup.send(f'Your partner ({partner.name}) is already in a study session! They need to quit it before joining another!')
                return
            else:
                partners.append(partner.id)

        partners.append(user_id)
        for partner in partners:
            study_sessions[partner] = {subject: {'start_time': datetime.now(timezone.utc), 'partners': partners, 'creator': user_id}}

        await interaction.followup.send(f'Timer started successfully! Study subject: "{subject}". Member in the group: {unvalidated_partner}')

    # End a study session
    @tree.command(name='endstudy', description='Finish a timer for a specific study subject already initialized')
    @app_commands.describe(subject='Finish subject')
    async def endstudy(interaction: discord.Interaction, subject: str):
        await interaction.response.defer()

        user_id = interaction.user.id

        if user_id not in study_sessions:
            await interaction.followup.send('You are not in a study session yet! Join one!')
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
            await interaction.followup.send('You have no ended sessions!')
            return

        if subject not in ended_sessions[user_id]:
            await interaction.followup.send(f'There are no ended sessions named "{subject}"!')
            return

        formatted_time = format_study_duration(ended_sessions[user_id][subject])
        await interaction.followup.send(f'Time spent on "{subject}":  {formatted_time}')    
