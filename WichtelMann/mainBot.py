import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands, tasks
import re
import random
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Channel IDs:
#   id=796051477738684428 // wichtelchat
#   id=796376465741840444 // bot-test
#   id=796393926826655754 // geburtsdaten
#   id=796390311168835607 // wanderwichtelanmeldung

#Initialisiert den Bot und die Variablen zum Programmstart
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
   birthdayList = [[],[],[]] # [0] name, [1] birthday, [2] giftbringer

#   check_for_birthdays_once_a_day.start()

#@tasks.loop(hours=24)
#async def check_for_birthdays_once_a_day():
#    curDate = datetime.now()
#    curDate = curDate.strftime("%d.%m")
#    print(curDate)

#    for birthday in birthdayList[1]:
#        print(str(birthday - curDate))
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Debug zum Connectioncheck
    if message.content == 'Hi':
        await message.channel.send("Ho")

    # Nachrichten im Bot Befehle Channel
    if message.channel == channel_wichtelBotBefehle:
        
        # Gibt die Befehle aus
        if(message.content == 'help'):
            await message.channel.send("\nDie Befehle sind:\n\troll again -> Startet die zufällige Ziehnung\n\tshow rolls -> Gibt die aktuellen Ziehungen aus")

        # Zieht zufällig die Wichtelpaare und speichert sie in der txt-Datei
        if(message.content == 'roll again'):
            with open("birthdays.txt", 'r') as file: # Parst die Datei birthdays.txt
                lines = file.readlines()
                birthdayList[0].clear()
                birthdayList[1].clear()
                birthdayList[2].clear()
                for line in lines:
                    line = line.replace("\n", "")
                    name, birthday, selectedPicker = line.split(':')
                    tmpBirthdayArray = birthday.split('.')
                    birthdayDateTime = datetime.datetime(2020, int(tmpBirthdayArray[1]), int(tmpBirthdayArray[0])) # Geburtstag als datetime
                    birthdayDateTime = birthdayDateTime.strftime("%d.%m")
                    if(selectedPicker != ""):
                        birthdayList[2].append(selectedPicker)
                    birthdayList[0].append(name)
                    birthdayList[1].append(birthdayDateTime)

            namesInList = ""
            selection = ""

            # Summiert die Namen mit Geburtstagen und LineBreaks zu einem String
            for index in range(len(birthdayList[0])): 
                namesInList += birthdayList[0][index] + " : " + birthdayList[1][index] + "\n"
            
            if(birthdayList[2][0] != ""):
                # Random shuffeling
                selbergezogen = True

                while selbergezogen:
                    selbergezogen = False
                    birthdayList[2] = birthdayList[0].copy()
                    random.shuffle(birthdayList[2])
                
                    for i in range(len(birthdayList[0])): # Man darf sich nicht selber ziehen
                        if(birthdayList[0][i] == birthdayList[2][i]):
                            selbergezogen = True

            # Output Ziehung
            for index in range(len(birthdayList[0])): 
                selection += birthdayList[0][index] + " : " + birthdayList[2][index] + "\n"

            output = "############\nIn der Ziehung enthalten sind:\n\n"
            output += namesInList
            output += "#######################\n"
            output += "Die Ziehung hat ergeben:\n(Beschenkter : Geschenkebringer)\n\n"
            output += selection
            output += "#######################"
            await message.channel.send(output)

            # Save rolls
            with open("birthdays.txt", "w") as file:
                for i in range(len(birthdayList[0])):
                    file.write(birthdayList[0][i] + ":" + birthdayList[1][i] + ":" + birthdayList[2][i] + "\n")

        # Gibt die aktuellen Ziehungen aus
        if(message.content == 'show rolls'):
            with open("birthdays.txt", 'r') as file: # Parst die Datei birthdays.txt
                lines = file.readlines()
                birthdayList[0].clear()
                birthdayList[1].clear()
                birthdayList[2].clear()
                for line in lines:
                    line = line.replace("\n", "")
                    name, birthday, selectedPicker = line.split(':')
                    tmpBirthdayArray = birthday.split('.')
                    birthdayDateTime = datetime.datetime(2020, int(tmpBirthdayArray[1]), int(tmpBirthdayArray[0])) # Geburtstag als datetime
                    birthdayDateTime = birthdayDateTime.strftime("%d.%m")
                    if(selectedPicker != ""):
                        birthdayList[2].append(selectedPicker)
                    birthdayList[0].append(name)
                    birthdayList[1].append(birthdayDateTime)

            namesInList = ""
            selection = ""
            
            for index in range(len(birthdayList[0])): 
                namesInList += birthdayList[0][index] + " : " + birthdayList[1][index] + "\n"
            for index in range(len(birthdayList[0])): 
                selection += birthdayList[0][index] + " : " + birthdayList[2][index] + "\n"

            output = "############\nIn der Ziehung enthalten sind:\n\n"
            output += namesInList
            output += "#######################\n"
            output += "Die Ziehung hat ergeben:\n(Beschenkter : Geschenkebringer)\n\n"
            output += selection
            output += "#######################"
            await message.channel.send(output)

        
            

    # Geburtsdatum in Channel Geburtsdaten eingeben und in Textdatei speichern
    if message.channel == channel_geburtsdaten:
        if re.search(r"^[0-9]{2}\.[0-9]{2}$", message.content):
            date = message.content.split('.')
            if(int(date[0]) <= 31):
                if(int(date[1]) <=12):
                    await message.author.remove_roles(get(message.author.guild.roles , name='Wichtel-Wanderer_unbestaetigt'))
                    await message.author.add_roles(get(message.author.guild.roles , name='Wichtel-Wanderer'))
                    with open("birthdays.txt", "a") as file:
                        file.write(str(message.author) + ":" + message.content + ":\n")
                else:
                    await message.delete()
            else:
                await message.delete()
        else:
            await message.delete()

    # Channel ID zum debuggen ausgeben
    if message.content == 'get_channel_id':
        print(message)
        
# Verteilt Rollen, wenn man mit einem Geschenk reacted
@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.emoji == '🎁':
        await user.add_roles(get(user.guild.roles , name='Wichtel-Wanderer_unbestaetigt'))
        await user.remove_roles(get(user.guild.roles , name='Wichtel-Wanderer'))
        await channel_wichtelchat.send('{0} ist jetzt beim Wichteln dabei, Gratulation!!'.format(user))

client.run(TOKEN)