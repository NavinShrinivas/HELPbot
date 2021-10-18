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
 #this is a comment 1

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('$addteam'):
        if(if_perms("CORE",message)):
            print("adding teams command invoked")
            m1 = await message.channel.fetch_message(message.reference.message_id) #saving mods time
            print(m1.content)
            l1=m1.content.split(" ")
            print(l1)
            if(len(l1) <= 1 ) :
                await m1.reply("Wrong format!")
            elif (l1[0][0] != "<"): #checks for tagged members
                await m1.reply("You have not mentioned team members to assign role to")
            elif(l1[-1][0]=="<"): ## checks is the command ends with team name
                await m1.reply("You have not given a team name to assign")
            else:
                guild = message.guild
                new_role=l1[-1]
                flag=1
                for i in message.guild.roles:
                    if i.name == new_role:
                        flag=0
                if (flag==0):
                    pass
                    await m1.reply("Role already exists ! only adding team members.")
                else:
                    await guild.create_role(name=l1[-1])
                    teamname = "-----"+l1[-1]+"------"
                    category = await guild.create_category(teamname, overwrites=None, reason=None)
                    for i in message.guild.roles:
                        await category.set_permissions(i, read_messages=False, connect=False)
                    await category.set_permissions(get(message.guild.roles, name=new_role) , send_messages=True, connect=True, speak=True)

                    await guild.create_voice_channel(f"Team-VC", overwrites=None, category=category, reason=None)
                    await guild.create_text_channel(f'Team-Chat', category=category)


                role=get(message.guild.roles, name=new_role)
                c=[]
                for i in range(0,(len(l1)-1)):
                    c.append(l1[i])
                await message.channel.send("done adding role to:")
                for user in c:
                    for alluser in message.guild.members:
                        if(str(alluser.id)==user[3:-1]): 
                            await alluser.add_roles(role) #adding the role
                            await message.channel.send(alluser)
                await m1.reply("created team with everyone tagged in this message")
        else:
            await message.channel.send("You dont have enuf perms sur!")

    role_prent = 0;
    if message.content.startswith('$delrole'): 
        print("deleting roles was invoked")
        if(if_perms("CORE",message)):
            l1=message.content.split(" ")
            print(l1)
            delrole=l1[1]
            while role_exist(delrole,message):
                role_prent = 1
                role_object = discord.utils.get(message.guild.roles, name=delrole)
                await role_object.delete()
                await message.channel.send("role has been deleted")
            
            if role_exist(delrole,message)==False and role_prent == 0:
                await message.channel.send("Role was not present in this server")

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
