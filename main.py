import discord
import os
import decouple
from dotenv import load_dotenv



client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('I AM IN THE MATRIX [logged in]')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$addteam'):
        l1=message.content.split(" ")
        guild = message.guild
        await guild.create_role(name=l1[len(l1)-1])
        


client.run(TOKEN)
