import discord
import os
import decouple
from dotenv import load_dotenv
from discord.utils import get

intents = discord.Intents.all()
client = discord.Client(intents=intents)

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
        if(if_perms("admin",message) or if_perms("technical",message)):
            print("adding teams command invoked")
            l1=message.content.split(" ")
            print(l1)
            if (l1[1][0] != "<"):
                await message.channel.send("You have not mentioned team members to assign role to")
            elif(l1[-1][0]=="<"):
                await message.channel.send("You have not given a team name to assign")
            else:
                guild = message.guild
                new_role=l1[-1]
                flag=1
                for i in message.guild.roles:
                    if i.name == new_role:
                        flag=0
                if (flag==0):
                    pass
                    await message.channel.send("Role already exists ! only adding team members.")
                else:
                    await guild.create_role(name=l1[-1])

                role=get(message.guild.roles, name=new_role)
                c=[]
                for i in range(1,(len(l1)-1)):
                    c.append(l1[i])
                await message.channel.send("done adding role to:")
                for user in c:
                    for alluser in message.guild.members:
                        if(str(alluser.id)==user[3:-1]):
                            await alluser.add_roles(role)
                            await message.channel.send(alluser)
                await message.channel.send("done with all members")
        else:
            await message.channel.send("You dont have enuf perms sur!")


    if message.content.startswith('$delrole'): 
        print("deleting roles was invoked")
        if(if_perms("admin",message) or if_perms("technical",message)):
            l1=message.content.split(" ")
            print(l1)
            delrole=l1[1]
            while role_exist(delrole,message):
                role_object = discord.utils.get(message.guild.roles, name=delrole)
                await role_object.delete()
                await message.channel.send("role has been deleted")
            
            if role_exist(delrole,message)==False:
                await message.channel.send("Role has be removed or was not present in this server")

def if_perms(role,message):
    flag=0
    for i in message.author.roles:
        if i.name==role:
            flag=1
    if flag==1:
        return True
    else:
        return False

def role_exist(role,message):
    flag=0
    for i in message.guild.roles:
        if i.name==role:
            flag=1
    if flag==1:
        return True
    else:
        return False

client.run(TOKEN)