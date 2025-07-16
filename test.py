import discord
from discord import app_commands
from discord.ext import commands

import asyncio
from datetime import datetime, timezone
import os

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot('.', intents=intents)
i = 0

# Inicialização
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'Comando sincronizados: {len(synced)}')
    print('Tudo ok!')

# Faz um saudação
greetings_words = ['oi', 'ola', 'olá', 'eae', 'salve', 'hi', 'hello']

@bot.event
async def on_message(message:discord.Message):
    if message.author.bot:
        return
    
    user = message.author.name

    if any(word in message.content.lower() for word in greetings_words):
        if message.author.id == 1058153961288388709:
            await message.reply(f'Vai se fuder {user}') 
        else:   
            await message.reply(f'Salve salve {user}')
    
    if message.author.id == 1058153961288388709:
        global i
        i += 1
        await message.reply(f'Aviso de time out {i}/3')
            
        if i == 3:
           nick_antigo = message.author.nick
           await message.reply(f'Se fudeu')
           await message.author.edit(nick="Castigada 🤡") 
           i = 0

           await asyncio.sleep(5)
           await message.author.edit(nick=f'{nick_antigo}')   

@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    print(f"[DEBUG] Algo mudou na presença de {after.name}")

# Contador de tempo de atividade
atividade = {}
@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    antes = before.activity
    depois = after.activity

    if depois and not antes:
        atividade[after.id] = datetime.now(timezone.utc)
        print(f"{after.name} começou uma atividade às {atividade[after.id]}")

    elif antes and not depois:
        inicio = atividade.pop(after.id, None)
        if inicio:
            duracao = datetime.now(timezone.utc) - inicio
            print(f'{after.name} ficou em uma atividade por {duracao}')

# Escreve o que for pedido
@bot.tree.command(name='repetir', description='Repete uma mensagem')
@app_commands.describe(texto='Texto que o bot vai repetir')
async def repetir(interaction: discord.Interaction, texto: str):
    await interaction.response.send_message(texto)    

# Renomeia o apelido do membro
@bot.tree.command(name='renomear', description='Define um novo apelido a um membro do servidor')
@app_commands.describe(membro='Membro que terá um novo apelido', apelido='Apelido que o bot dará')
async def renomear(interaction: discord.Interaction, membro: discord.Member, apelido: str):
    await membro.edit(nick=apelido)
    await interaction.response.send_message(f'Agora {membro} se chama {apelido}')

# Desconecta um membro    
@bot.tree.command(name='desconectar', description='Desconecta um membro da ligação')
@app_commands.describe(membro='Membro que será desconectado')
async def desconectar(interaction: discord.Interaction, membro: discord.Member):
   canal = membro.voice.channel
   await membro.move_to(None)
   await interaction.response.send_message(f'{membro} foi desconectado da call {canal}')

# Move o membro de call    
@bot.tree.command(name='mover', description='Move um membro de uma call para outra')
@app_commands.describe(membro1='Membro que será movido', membro2='Membro que será movido', membro3='Membro que será movido', membro4='Membro que será movido', membro5='Membro que será movido', call='Canal de voz destinado')
async def mover(
    interaction: discord.Interaction,
    call: discord.VoiceChannel, 
    membro1: discord.Member,
    membro2: discord.Member = None,
    membro3: discord.Member = None, 
    membro4: discord.Member = None, 
    membro5: discord.Member = None, 
):

    membros = [membro1]
    if membro2:
        membros.append(membro2)
    if membro3:
        membros.append(membro3)
    if membro4:
        membros.append(membro4)
    if membro5:
        membros.append(membro5)

    for membro in membros:

        await membro.move_to(call)
    await interaction.response.send_message(f'Todos os membros foram movidos com sucesso para {call}')    


# Silencia voz de um membro
@bot.tree.command(name='silenciar', description='Silencia o microfone de um membro')
@app_commands.describe(membro='Membro que será silenciado')
async def silenciar(interaction: discord.Interaction, membro: discord.Member):
    if membro.voice is None:
        await interaction.response.send_message(f'{membro} não esta em nenhum canal de voz', ephemeral=True)
        return

    if membro.voice.mute == False:
        await membro.edit(mute=True)
        await interaction.response.send_message(f'{membro} foi mutado com sucesso')
    else:
        await membro.edit(mute=False)
        await interaction.response.send_message(f'{membro} foi desmutado com sucesso')

# Desativa áudio de um membro
@bot.tree.command(name='desativar_audio', description='Desativa o áudio de um membro')
@app_commands.describe(membro='Membro que terá o áudio desativado')
async def desativar_audio(interaction: discord.Interaction, membro: discord.Member):
    if membro.voice is None:
        await interaction.response.send_message(f'{membro} não esta em nenhum canal de voz', ephemeral=True)
        return
    
    if membro.voice.deaf == False:
        await membro.edit(deafen=True)
        await interaction.response.send_message(f'{membro} teve o áudio desativado com sucesso')
    else:
        await membro.edit(deafen=False)
        await interaction.response.send_message(f'{membro} teve o áudio ativado com sucesso')


bot.run(os.getenv('TOKEN'))