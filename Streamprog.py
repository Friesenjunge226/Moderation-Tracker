import os
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import subprocess
from dotenv import load_dotenv
from datetime import datetime, time
import requests
import random
import configparser
import winsound

config = configparser.ConfigParser()
config.read("config.conf")

# Read settings from config file


CurrentVersion = config["SETTINGS"]["CurrentVersion"].strip()
TARGET_CHANNEL = config["SETTINGS"]["TargetChannel"]
ShowDebugMessages = config["SETTINGS"].getboolean("ShowDebugMessages")
IsHoliday = config["SETTINGS"]["IsHoliday"]
AutoLogoffTime = config["SETTINGS"]["AutoLogoffTime"]
UseLoggedLoveScores = config["SETTINGS"].getboolean("UseLoggedLoveScores")
PlayMessageSoundEffects = config["SETTINGS"]["PlayMessageSoundEffects"]
CheckForUpdatesOnStartup = config["SETTINGS"].getboolean("CheckForUpdatesOnStartup")
UpdateCheckURL = config["SETTINGS"]["UpdateCheckURL"]
UseChatCommands = config["SETTINGS"].getboolean("UseChatCommands")
LOVE_FILE = config["SETTINGS"]["LoveScoreFile"]
CheckInterval = config["SETTINGS"].getint("CheckInterval")
WATCHLIST = config["SETTINGS"]["WatchedModerators"].split(",")
BOTS = config["SETTINGS"]["BotNames"].split(',')
KeyFile = config["SETTINGS"]["KeyFile"]
USER_SCOPE = config["SETTINGS"]["UserScopes"].split(",")

if ShowDebugMessages == True:
    print(f"[DEBUG] {CurrentVersion}")
    print(f"[DEBUG] {TARGET_CHANNEL}")
    print(f"[DEBUG] {ShowDebugMessages}")
    print(f"[DEBUG] {IsHoliday}")
    print(f"[DEBUG] {AutoLogoffTime}")
    print(f"[DEBUG] {UseLoggedLoveScores}")
    print(f"[DEBUG] {PlayMessageSoundEffects}")
    print(f"[DEBUG] {CheckForUpdatesOnStartup}")
    print(f"[DEBUG] {UpdateCheckURL}")
    print(f"[DEBUG] {UseChatCommands}")
    print(f"[DEBUG] {LOVE_FILE}")
    print(f"[DEBUG] {CheckInterval}")
    print(f"[DEBUG] {WATCHLIST}")
    print(f"[DEBUG] {BOTS}")
    print(f"[DEBUG] {KeyFile}")
    print(f"[DEBUG] {USER_SCOPE}")
    # Define Variables
    noticeme = ""
    logged_in_mods = []

print(f"Chatbot and Moderator Tracker for the channel {TARGET_CHANNEL}")
            
load_dotenv(dotenv_path=KeyFile)  # reads variables from a .env file and sets them in os.environ

APP_ID = os.getenv("APP_ID") # ID of ther bot
APP_SECRET = os.getenv("APP_SECRET") # Token of the bot
TOKEN = os.getenv("TOKEN") # The access token of the IRC connection
BOTNAME = os.getenv("BOTNAME") # The Name of the bot using the IRC Connection
BROADCASTER_ID = os.getenv("BROADCASTER_ID") # The User ID of the channel the bot is running on. You can find this by using a Twitch API endpoint or by using a tool like Twitch Inspector.
YTMD_TOKEN = os.getenv("YTMD_TOKEN") # The access token for the YTMDesktop API, only needed if you want to use the music features of the bot

if CheckForUpdatesOnStartup == True:
    url = f"{UpdateCheckURL}"
    response = requests.get(url)

    LnOne = response.text.split('\n')[1]
    LastestVersion = LnOne.split('=')[0].strip()
    if ShowDebugMessages == True:
        print(f"Latest version: {LastestVersion}, Current version: {CurrentVersion}")
    if response.status_code == 200:
        if str(LastestVersion) == str(CurrentVersion):
            print("You are running the latest version.")
        else:
            print(f"An update is available! Current version: {CurrentVersion}, Latest version: {LastestVersion}\n")
            print("Please visit the GitHub repository to download the latest version.\n")
    elif response.status_code == 404:
        print("Update check URL not found (404). Please check the UpdateCheckURL in the config file.")
    elif response.status_code == 500:
        print("Internal server error (500) when checking for updates. Please try again later.")
    else:
        print("Failed to check for updates with the response code", response.status_code)
        print("More information: can be found on the Wikipedia article about HTTP response status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes")
        if ShowDebugMessages == True:
            print(f"[DEBUG] Update check response: {response.text}")
else:
    if ShowDebugMessages == True:
        print("[DEBUG] Update check on startup is disabled, skipping update check")


async def main():
    
    # create tasks for the things to run
    # This is where you can add more things to run in parallel
    task1 = asyncio.create_task(run()) # Start the Chatbot

    await asyncio.gather(task1) # Run the things specified above
    if ShowDebugMessages == True:
        print("[DEBUG] Main tasks started")

async def push():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "-m", f"Auto update {ts}"])
    subprocess.run(["git", "push", "origin", "main"])
    if ShowDebugMessages == True:
        print("[DEBUG] Changes pushed to remote repository")



# called on bot start
async def on_ready(ready_event: EventData):
    print('[TwitchAPI] Bot is ready for work, joining channels...')
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # bot init


# this will be called whenever a message in a channel was sent by either the bot OR another user
async def on_message(msg: ChatMessage):
    if not msg.user.name in BOTS:
        print(f'[TwitchAPI] in {msg.room.name}, {msg.user.name} said: {msg.text}')
        if PlayMessageSoundEffects == True:
            winsound.PlaySound("yes.wav", winsound.SND_FILENAME)

    


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')
    


async def ping(cmd: ChatCommand):
    if cmd.user.name in WATCHLIST or cmd.user.name == TARGET_CHANNEL:
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
    if cmd.user.name in logged_in_mods or cmd.user.name in noticeme:
        with open(LOGFILE, "a") as logfile:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logfile.write(f"[{ts}] {cmd.user.name} PART\n")
            push()
    
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
    if UseLoggedLoveScores == True:
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
        
async def ModCheck(logged_in_mods, Noticeme):
    """This function is called to start the periodic moderator status checks"""
    




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
    if UseChatCommands == True:
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
        if ShowDebugMessages == True:
            print("[DEBUG] Commands registered")
    else:
        if ShowDebugMessages == True:
            print("[DEBUG] Chat commands disabled, skipping command registration")

    
    
    # we are done with our setup, lets start this bot up!
    chat.start()
    if ShowDebugMessages == True:
        print("[DEBUG] Bot started!")

# run setup
asyncio.run(main())