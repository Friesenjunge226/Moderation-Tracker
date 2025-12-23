import os
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import subprocess
from dotenv import load_dotenv
import aiohttp
import os
import pygame
from datetime import datetime, time
import requests
#import atexit

load_dotenv(dotenv_path="C:/Users/DerFriese/Moderation-Tracker/keys.env")  # reads variables from a .env file and sets them in os.environ

APP_ID = os.getenv("APP_ID") # ID of ther bot
APP_SECRET = os.getenv("APP_SECRET") # Token of the bot
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT] # Permissions the chatbot should have
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL") # Target channel
TOKEN = os.getenv("TOKEN") # The access token of the IRC connection
BOTNAME = os.getenv("BOTNAME") # The Name of the bot using the IRC Connection
LOGFILE = os.getenv("LOGFILE") # The file the Script writes to
PUSH_INTERVAL = 5 # The interval in which the Script pushes data to the githhub repository in Seconds
BROADCASTER_ID = os.getenv("BROADCASTER_ID")

WATCHLIST = ["mo_ju_rsck","yinnox98_live","meliorasisback","Friesenjunge226"]  # Users to be Monitored
BOTS = [TARGET_CHANNEL,"streamelements","moobot","nightbot","wizebot","ankhbot","phantombot","coebot","vercix","kappa_genius","streamlabs","streamloots"]  # Users to be excluded from tracking e.g. Bots
HOLIDAYS = False # Disable automatic mod checkout after 21:00 on holidays



print(f"Chatbot and Moderator Tracker for the channel {TARGET_CHANNEL}")


async def main():
    #task1 = asyncio.create_task(log_mods()) # Start the IRC Connection
    task2 = asyncio.create_task(run()) # Start the Chatbot

    await asyncio.gather(task2) # Run the things specified above


async def log_mods():
    while True:
        url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={BROADCASTER_ID}&moderator_id={BROADCASTER_ID}"
        headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Client-ID": "1618fy8fq7wba32p612v6998zaz6c9"
}
        response = requests.get(url, headers=headers)
        
        #print(response.text) # For debugging purposes
        
        data = response.json()
        
        usernames = [user['user_login'] for user in data['data']]
        Mods = set(usernames).intersection(WATCHLIST)
        #print(f"Mods currently in Chat: {Mods}") # For debugging purposes
        with open(LOGFILE, "a") as f:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{ts}\n")
    
        
        
        
async def push():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "-m", f"Auto update {ts}"])
    subprocess.run(["git", "push", "origin", "main"])



# called on bot start
async def on_ready(ready_event: EventData):
    print('[TwitchAPI] Bot is ready for work, joining channels...')
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # bot init


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    if not msg.user.name in BOTS:
        print(f'[TwitchAPI] in {msg.room.name}, {msg.user.name} said: {msg.text}')
        pygame.mixer.init()
        pygame.mixer.music.load("yes.mp3")
        pygame.mixer.music.play()

    


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')
    


async def ping(cmd: ChatCommand):
    await cmd.reply('pong')

async def Andy(cmd: ChatCommand):
    await cmd.reply("WEEWOO Alarm Alarm ein Andy nähert sich dem Stream WEEWOO")
    
async def Fr226(cmd: ChatCommand):
    await cmd.reply("Der Friese ist da :3!")

async def Larsi(cmd: ChatCommand):
    await cmd.reply("Achtung Achtung. Platz daaa! Larsi ist da")

async def Liebe(cmd: ChatCommand):
    await cmd.reply("<3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3")
    
async def Mo(cmd: ChatCommand):
    await cmd.reply("Mo sagt Halli")
    
async def Apex(cmd: ChatCommand):
    await cmd.reply("Apex ist hier, um deinen Stream wegzuzaubern!")

async def banger(cmd: ChatCommand):
    await cmd.reply("Was ein Banger DinoDance DinoDance DinoDance")
    
async def bye(cmd: ChatCommand):
    await cmd.reply("peepoBye peepoBye peepoBye")
    
async def discord(cmd: ChatCommand):
    await cmd.reply("Trete gerne meinem Community Discord Server bei, um keinen Stream mehr zu verpassen -> https://discord.com/invite/b77hdjUuyX")
    
async def hl(cmd: ChatCommand):
    await cmd.reply("Hallo, willkommen im Chat HYPERS ! Schön, dass du da bist.")
    
async def kohl(cmd: ChatCommand):
    await cmd.reply("Der Kohl übernimmt die Welt!!!!")
    
async def noot(cmd: ChatCommand):
    await cmd.reply("°o° Noot Noot peepoCheer")
    
async def shader(cmd: ChatCommand):
    await cmd.reply("Friesenjunge nutzt den Complementary Reiminagined Shader!")
    
async def trinken(cmd: ChatCommand):
    await cmd.reply("Alle Trinken jetzt nen Schluck. Prost.")
    
async def whatsapp(cmd: ChatCommand):
    await cmd.reply("Ich hab nun nen Channel :3 Kommt gerne rein! Es ist alles anonym -> https://whatsapp.com/channel/0029Vb68Cm71Xquc5Ay6qv2y")
    
async def lurk(cmd: ChatCommand):
    await cmd.reply(f"@{cmd.user.name} ist nun im lurk. Viel spaß :D")
    
async def unlurk(cmd: ChatCommand):
    await cmd.reply(f"@{cmd.user.name} ist wieder im Chat. Halli :D")
    
async def pain(cmd: ChatCommand):
    await cmd.reply(f"@{cmd.user.name} will nicht mehr. @{cmd.user.name} hält das alles nicht mehr aus. @{cmd.user.name} hasst gerade alles Madge .")

async def aua(cmd: ChatCommand):
    await cmd.reply(f"@{cmd.user.name} hat gerade große Schmerzen")
    
async def test(cmd: ChatCommand):
    await cmd.reply(f"Test, Test. eins, zwei, drei. Test erfolgreich")

    
# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)
    
    print(f"[TwitchAPT] Startup Finished. Connected.")
    
    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('ping', ping)
    chat.register_command("Andy", Andy)
    chat.register_command("Friese", Fr226)
    chat.register_command("Larsi", Larsi)
    chat.register_command("Liebe", Liebe)
    chat.register_command("Mo", Mo)
    chat.register_command("Apex", Apex)
    chat.register_command("Banger", banger)
    chat.register_command("bye", bye)
    chat.register_command("dc", discord)
    chat.register_command("discord", discord)
    chat.register_command("hl", hl)
    chat.register_command("kohl", kohl)
    chat.register_command("wargamer", kohl)
    chat.register_command("nootnoot", noot)
    chat.register_command("shader", shader)
    chat.register_command("trinken", trinken)
    chat.register_command("whatsapp", whatsapp)
    chat.register_command("wa", whatsapp)
    chat.register_command("lurk", lurk)
    chat.register_command("unlurk", unlurk)
    chat.register_command("pain", pain)
    chat.register_command("aua", aua)
    chat.register_command("test", test)

    
    
    # we are done with our setup, lets start this bot up!
    chat.start()

# run setup
asyncio.run(main())