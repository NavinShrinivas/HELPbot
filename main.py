import discord
import os
import decouple
from dotenv import load_dotenv
# from discord.ext.commands import author
# from discord import author


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
        for i in l1:
            await message.channel.send(i)
        


client.run(TOKEN)
