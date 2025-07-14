import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot('.', intents=intents)

# Inicialização
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'Comando sincronizados: {len(synced)}')
    print('Tudo ok!')

@bot.tree.command(name='ola', description='Envia um "oi"')
async def ola(interaction:discord.Interaction):
    user = interaction.user.name
    if interaction.user.id == 1058153961288388709:
        await interaction.response.send_message(f'Vai se fuder {user}') 
    else:   
        await interaction.response.send_message(f'Salve salve {user}')

@bot.tree.command(name='repetir', description='Repete uma mensagem')
@app_commands.describe(texto='Texto que o bot vai repetir')
async def repetir(interaction:discord.Interaction, texto: str):
    await interaction.response.send_message(texto)



bot.run('MTM5NDM2MDE0NzA4OTgyMTc3Ng.GU5fkH.s9IO68VlTNJjI5dgEzeSFvGPaMNicHfX_ZlQt0')