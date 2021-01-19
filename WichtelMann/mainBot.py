import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Channel IDs:
#   id=796051477738684428 // wichtelchat
#   id=796376465741840444 // bot-test
#   id=796393926826655754 // geburtsdaten
#   id=796390311168835607 // wanderwichtelanmeldung


@client.event
async def on_ready():
   print(f'{client.user} has connected to Discord!')

   # Channeldefinition
   global channel_wichtelchat
   global channel_bot_test
   global channel_geburtsdaten
   global channel_wanderwichtelanmeldung
   global channel_wichtelBotBefehle
   global birthdayList

   channel_wichtelchat = client.get_channel(796051477738684428)
   channel_bot_test = client.get_channel(796376465741840444)
   channel_geburtsdaten = client.get_channel(796393926826655754)
   channel_wanderwichtelanmeldung = client.get_channel(796390311168835607)
   channel_wichtelBotBefehle = client.get_channel(796441844933460059)
   birthdayList = []

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'Hi':
        await message.channel.send("Ho")

    # Nachrichten im Bot Befehle Channel
    if message.channel == channel_wichtelBotBefehle:
        
        if(message.content == 'help'):
            await message.channel.send("\nDie Befehle sind:\n\troll -> Startet die zufällige Ziehnung")
        if(message.content == 'roll'):
            with open('birthdays.txt', "r") as f:
                lines = f.readlines()
                print(lines)
                for line in lines:
                    name, birthday = line.split(':')
                    #nameLst = []
                    #birthdayLst = []
                    #nameLst.append(name)
                    #birthdayLst.append(birthday)
                    print(line)
                    print(name)
                    print(birthday)
                    birthdayList[0].append(name)
                    birthdayList[1].append(birthday)
                print(birthdayList)

    # Geburtsdatum in Channel Geburtsdaten eingeben und in Textdatei speichern
    if message.channel == channel_geburtsdaten:
        if re.search(r"^[0-9]{2}\.[0-9]{2}\.$", message.content):
            date = message.content.split('.')
            if(int(date[0]) <= 31):
                if(int(date[1]) <=12):
                    await message.author.remove_roles(get(message.author.guild.roles , name='Wichtel-Wanderer_unbestaetigt'))
                    await message.author.add_roles(get(message.author.guild.roles , name='Wichtel-Wanderer'))
                    with open("birthdays.txt", "a") as file:
                        file.write(str(message.author) + ":" + message.content + "\n")
                else:
                    await message.delete()
            else:
                await message.delete()
        else:
            await message.delete()

    if message.content == 'get_channel_id':
        print(message)
        

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if str(reaction.emoji) == '🎁':
        await user.add_roles(get(user.guild.roles , name='Wichtel-Wanderer_unbestaetigt'))
        await user.remove_roles(get(user.guild.roles , name='Wichtel-Wanderer'))
        await channel_wichtelchat.send('{0} ist jetzt beim Wichteln dabei, Gratulation!!'.format(user))

client.run(TOKEN)