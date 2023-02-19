import os
import discord
from dotenv import load_dotenv

import command
import confdb

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

conf_man = confdb.ConfManager()

botReady = False

@client.event
async def on_ready():
    global botReady
    print(f'Logged on as {client.user}!')
    await client.change_presence(activity=discord.Game(name="Setting up bot"))
    
    for guild in client.guilds:
        conf_man.init_db(guild.id)
    
    botReady = True
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="commands"))
    

@client.event
async def on_message(message: discord.Message):
    global botReady
    if botReady:
        await command.interpret_command(message, conf_man)

@client.event
async def on_guild_join(guild: discord.Guild):
    print("[bot] was added to a new guild")
    confdb.init_db(guild.id)

client.run(os.getenv("token"))