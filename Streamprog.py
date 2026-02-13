import os
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import subprocess
from dotenv import load_dotenv
import pygame
from datetime import datetime, time
import requests
import random
import configparser

       
config = configparser.ConfigParser()
config.read("config.conf")

# Read settings from config file
settings = config['SETTINGS']
CurrentVersion = settings.get('CurrentVersion')
TARGET_CHANNEL = settings.get('TargetChannel')
ShowDebugMessages = settings.getboolean('ShowDebugMessages')
IsHoliday = settings.get('IsHoliday')
AutoLogoffTime = settings.get('AutoLogoffTime')
UseLoggedLoveScores = settings.getboolean('UseLoggedLoveScores')
PlayMessageSoundEffects = settings.getboolean('PlayMessageSoundEffects')
if PlayMessageSoundEffects == "True":
        pygame.mixer.init()
if ShowDebugMessages == "True":
                    print("[DEBUG] Sound effects initalized")
else:
    if ShowDebugMessages == "True":
        print("[DEBUG] Sound effects disabled, Skipping Sound initalization")

CheckForUpdatesOnStartup = settings.getboolean('CheckForUpdatesOnStartup')
UpdateCheckURL = settings.get('UpdateCheckURL')
UseChatCommands = settings.getboolean('UseChatCommands')
LOVE_FILE = settings.get("LoveScoreFile")
CheckInterval = settings.getint("CheckInterval")
WATCHLIST = settings.get("WatchedModerators").split(",")
BOTS = settings.get('BotNames').split(',')
KeyFile = settings.get('KeyFile')

            
            
            
print(f"Chatbot and Moderator Tracker for the channel {TARGET_CHANNEL}")
            
load_dotenv(dotenv_path=KeyFile)  # reads variables from a .env file and sets them in os.environ

APP_ID = os.getenv("APP_ID") # ID of ther bot
APP_SECRET = os.getenv("APP_SECRET") # Token of the bot
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT] # Permissions the chatbot should have
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL") # Target channel
TOKEN = os.getenv("TOKEN") # The access token of the IRC connection
BOTNAME = os.getenv("BOTNAME") # The Name of the bot using the IRC Connection
LOGFILE = os.getenv("LOGFILE") # The file the Script writes to
BROADCASTER_ID = os.getenv("BROADCASTER_ID") # The Username of the channel the bot is running in

if CheckForUpdatesOnStartup == "True":
    url = f"{UpdateCheckURL}"
    response = requests.get(url)

    LnOne = response.text.split('\n')[0]
    LastestVersion = LnOne.split(':')[1].strip()
    if response.status_code == 200:
        if LastestVersion > CurrentVersion:
            print(f"An update is available! Current version: {CurrentVersion}, Latest version: {LastestVersion}\n")
            print("Please visit the GitHub repository to download the latest version.\n")
        elif LastestVersion == CurrentVersion: 
            if ShowDebugMessages == True:
                print(f"You are using the latest version: {CurrentVersion}\n")
        else:
            if ShowDebugMessages == True:
                print(f"You are using a newer version ({CurrentVersion}) than the latest release ({LastestVersion}).\n")
    else:
        print("Failed to check for updates. Status code:", response.status_code)


async def main():
    
    # create tasks for the things to run
    # This is where you can add more things to run in parallel
    task1 = asyncio.create_task(run()) # Start the Chatbot

    await asyncio.gather(task1) # Run the things specified above
    if ShowDebugMessages == "True":
        print("[DEBUG] Main tasks started")

async def push():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "-m", f"Auto update {ts}"])
    subprocess.run(["git", "push", "origin", "main"])
    if ShowDebugMessages == "True":
        print("[DEBUG] Changes pushed to remote repository")



# called on bot start
async def on_ready(ready_event: EventData):
    print('[TwitchAPI] Bot is ready for work, joining channels...')
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # bot init


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    if not msg.user.name in BOTS:
        print(f'[TwitchAPI] in {msg.room.name}, {msg.user.name} said: {msg.text}')
        if PlayMessageSoundEffects == "True":
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
    if cmd.user.name == "misterxpd_andy":
        await cmd.reply("WEEWOO Alarm Alarm ein Andy nähert sich dem Stream WEEWOO")
    
async def Fr226(cmd: ChatCommand):
    if cmd.user.name == "friesenjunge226":
        await cmd.reply("Der Friese ist da :3!")

async def Larsi(cmd: ChatCommand):
    if cmd.user.name == "knirpslarsi_":
        await cmd.reply("Achtung Achtung. Platz daaa! Larsi ist da")

async def Liebe(cmd: ChatCommand):
    await cmd.reply("<3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3")
    
async def Mo(cmd: ChatCommand):
    if cmd.user.name == "mo_ju_rsck":
        await cmd.reply("Mo sagt Halli")
    
async def Apex(cmd: ChatCommand):
    if cmd.user.name == "yinnox98_live":
        await cmd.reply("Apex ist hier, um deinen Stream wegzuzaubern!")

async def banger(cmd: ChatCommand):
    await cmd.reply("Was ein Banger DinoDance DinoDance DinoDance")
    
async def bye(cmd: ChatCommand):
    await cmd.reply("peepoBye peepoBye peepoBye")
    
async def discord(cmd: ChatCommand):
    await cmd.reply("Trete gerne meinem Community Discord Server bei, um keinen Stream mehr zu verpassen -> https://discord.com/invite/b77hdjUuyX")
    
async def hl(cmd: ChatCommand):
    await cmd.reply(f"Hallo, willkommen im Chat {cmd.user.name} HYPERS ! Schön, dass du da bist.")
    
async def kohl(cmd: ChatCommand):
    if cmd.user.name == "wargamer_live" or cmd.user.name == "wargamer2024":
        await cmd.reply("Der Kohl übernimmt die Welt!!!!")
    
async def noot(cmd: ChatCommand):
    await cmd.reply("°o° Noot Noot peepoCheer")
    
async def shader(cmd: ChatCommand):
    await cmd.reply("Friesenjunge226 nutzt den Complementary Reiminagined Shader!")
    
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
    if cmd.user.name in WATCHLIST or cmd.user.name == TARGET_CHANNEL:
        await cmd.reply(f"Test, Test. eins, zwei, drei. Test erfolgreich")
    
async def shutdown(cmd: ChatCommand):
    """Shutdown sequence"""
    if cmd.user.name in TARGET_CHANNEL or cmd.user.name in WATCHLIST:
        await cmd.send("Bot is shutting down...")
        
        try:
            with open(LOGFILE, 'r') as f:
                for mod in WATCHLIST:
                    f.write(f"")
        except FileNotFoundError:
            print(f"Log file not found: {LOGFILE}")
        
        # You an add any additional cleanup code here

        pygame.mixer.init()
        pygame.mixer.stop()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"Auto update {ts}"])
        subprocess.run(["git", "push", "origin", "main"])
        asyncio.get_event_loop().stop()
        exit
    else:
        await cmd.reply("Du bist nicht berechtigt, diesen Befehl zu nutzen.")


async def noticeme(cmd: ChatCommand):
    """This command marks the user as present and initiates periodic checks"""
    if cmd.user.name in WATCHLIST:
        await cmd.reply("Melde an...")
        with open(LOGFILE, "a") as logfile:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logfile.write(f"[{ts}] {cmd.user.name} JOIN")
            logged_in_mods = [mod for mod in WATCHLIST if f"{mod} JOIN" in logfile]
            Noticeme = cmd.user.name
            modcheck(logged_in_mods, Noticeme)
    else:
        await cmd.reply("Du bist nicht berechtigt, diesem Befehl zu nutzen.")
        
        
async def pride(cmd: ChatCommand):
    await cmd.reply("BisexualPride GayPride GenderFluidPride TransgenderPride PansexualPride NonbinaryPride IntersexPride AsexualPride LesbianPride BisexualPride VirtualHug")
    
async def cmdlist(cmd: ChatCommand):
    await cmd.reply("Alle commands: !Andy !Friese !Larsi !Liebe !Mo !Apex !Banger !bye !dc !dc !hl !kohl !nootnoot !shader !trinken !wa !lurk !unlurk !pain !aua !test !shutdown !pride !cmds")
    if cmd.user.name in WATCHLIST or cmd.user.name == TARGET_CHANNEL:
        await cmd.reply("Admin commands: !noticeme")

def load_love_scores(cmd:ChatCommand, user, target) -> dict:
    scores = {}

    if not os.path.exists(LOVE_FILE):
        cmd.chat("[WARNING] Love file not found")
        return scores

    with open(LOVE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            
            try:
                user, target, value = line.split("|", 2)
                pair = user, target
                scores[pair] = value
            except ValueError:
                continue

    return scores


def save_love_score(user, target, value: str):
    pair = user, target

    scores = load_love_scores()
    scores[pair] = value

    with open(LOVE_FILE, "w", encoding="utf-8") as f:
        for (u1, u2), v in scores.items():
            f.write(f"{u1}|{u2}|{v}\n")  
            
async def love(cmd: ChatCommand):
    if not cmd.parameter:
        await cmd.reply("Nutze den Befehl !love <Zielperson>, um die Liebe zwischen dir und der Zielperson zu überprüfen.")
        return

    user = cmd.user.name
    target = cmd.parameter

    pair = user, target
    scores = load_love_scores()

    # Bereits vorhanden -> aus Datei lesen
    if UseLoggedLoveScores == "True":
        if pair in scores:
            value = scores[pair]
        else:
            value = random.randint(0, 100)
            if value >= 95:
                value = random.randint(101, 1000)

            save_love_score(user, target, value)

        await cmd.reply(
            f"Die Liebe zwischen @{user} und {target} beträgt {value}%!"
    )

    
async def modcheck(logged_in_mods, Noticeme):
    """Check and log moderator status periodically"""
    
    while True:
        url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={BROADCASTER_ID}&moderator_id={BROADCASTER_ID}"
        headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Client-ID": APP_ID
}
        response = requests.get(url, headers=headers)
        data = response.json()
        usernames = [user['user_login'] for user in data['data']]
        Mods = set(usernames).intersection(logged_in_mods)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOGFILE, "a") as logfile:
            if Noticeme not in Mods:    
                logfile.write(f"[{ts}] {noticeme} PART\n")
                push()
        await asyncio.sleep(int(CheckInterval))  # Check every defined interval seconds



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


    # you can directly register commands and their handlers
    if UseChatCommands == "True":
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
        chat.register_command("shutdown", shutdown)
        chat.register_command("noticeme", noticeme)
        chat.register_command("pride", pride)
        chat.register_command("commands", cmdlist)
        chat.register_command("cmds", cmdlist)
        chat.register_command("love", love)
        if ShowDebugMessages == "True":
            print("[DEBUG] Commands registered")
    else:
        if ShowDebugMessages == "True":
            print("[DEBUG] Chat commands disabled, skipping command registration")

    
    
    # we are done with our setup, lets start this bot up!
    chat.start()
    if ShowDebugMessages == "True":
        print("[DEBUG] Bot strarted!")

# run setup
asyncio.run(main())