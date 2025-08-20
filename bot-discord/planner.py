import discord
from discord import app_commands

tasks = []

def register_planner(tree: app_commands.CommandTree):
    # Add a task
    @tree.command(name='task', description='Add a new task')
    @app_commands.describe(task='Add task')
    async def task(interaction: discord.Interaction, task: str):
        await interaction.response.defer()

        if task in tasks:
            await interaction.followup.send(f'There is already a task named "{task}" in progress!')
            return

        tasks.append(task)
        await interaction.followup.send(f'Task add successfully! Task: "{task}"')

    # Completes the task
    @tree.command(name='done', description='Mark a task as complete')
    @app_commands.describe(task='Complete task')
    async def done(interaction: discord.Interaction, task: str):
        await interaction.response.defer()

        if task not in tasks:
            await interaction.followup.send(f'There are no tasks named "{task}"!')
            return

        tasks.remove(task)
        await interaction.followup.send(f'{task} completed successfully! Good work!')

    # Shows the task list
    @tree.command(name='ongoing', description='Show ongoing tasks')
    async def ongoing(interaction: discord.Interaction):
        await interaction.response.defer()

        if not tasks:
            await interaction.followup.send('You have no tasks!')
            return

        await interaction.followup.send(tasks)    