# Moderation-Tracker

A simple Twitch Bot

## SETUP

The bot is written in Python and uses the Twitch API to track moderation actions in a Twitch channel. To set up the bot, follow these steps:

1. If not done already, install Python 3.10 or higher from [python.org](https://www.python.org/downloads/). 
2. Install all of the required dependencies by running the following command in your terminal:
   ```
   pip install -r requirements.txt
   ```
    If that for some reason dosen't work, you can try installing the dependencies one by one, using pip:
    ```
    pip install
    ```
    You need the following dependencies installed:

    | Dependency | Version |
    |------------|---------|
    | twitchAPI | >=4.5.0 |
    | asyncio | >=3.14.3 |
    | python-dotenv | >=1.2.1 |
    | requests | >=2.32.5 |
    | configparser | >=7.2.0 |
    | datetime | >=3.14.3 |


3. Create a Twitch Developer account and register an application to get your Client ID and Client Secret. You can do this at [Twitch Developer Console](https://dev.twitch.tv/console/apps).

4. Create a `.env` file in the root directory of the project and add your Twitch Client ID, Client Secret, and the channel you want to track. The `.env` file should look like this:
 

5. Tweak the `config.conf` file to your liking. You can change the list of watched moderators, the list of bot names, and the user scopes for the Twitch  API.

### Breakdown of the config.conf file

This file will be revisitited in the future, due to the settings being over the place right now.
| Setting | Description |
|---------|-------------|
|CurrentVersion| The current version of the bot. This is used for update checks and should NOT BE UPDATED, except if you know, what you're doing.
|Target Channel| The Twitch channel the bot should connect to. This should be the same as the TARGET_CHANNEL variable in the .env file. Multiple channels have not been tested yet.|
|ShowDebugMessages| If set to true, the bot will print debug messages to the console. This is useful for troubleshooting and development.|
|IsHoliday| If set, it disables the automatic mod logoff. This can be useful if you dont want the Moderators to be logged off automatically, for example during holidays.|
|AutoLogoffTime| The time in minutes after which the bot will automatically log off the moderators. This is only active if IsHoliday is set to false.|
|UseLoggedLoveScores| If srt to true, the bot will use the logged love scores in the love_scores.txt file. If false, it will regenerate the love scores every time the command is used.|
|PlayMessageSoundEffect| If set to true, the bot will play a sound effect when a message appears in chat. This can be useful to get notified, after a silent chat.|
|CheckForUpdatesOnStartup| If set to true, the bot will check for updates on startup. If an update is available, it will print a message in the console.|
|UpdateCheckURL| The URL the bot will use to check for updates. This URL should point to the config.conf file in a GitHub repository. This is uesful, if you maintain your own fork of the bot but still want to use the update check feature.|
|UseChatCommands| If set to true, the bot will respond to chat commands. The available commands are listed below.|
|LoveScoreFile| The file the bot will use to store the love scores. This is used to persist the love scores between restarts of the bot. This is only used if UseLoggedLoveScores is set to true.|
|CheckInterval| The interval in seconds at which the bot will check, if the moderators are still online.|
|WatchedModerators| A comma separated list of moderators the bot should track. The bot will log the activity of these users.|
|BotNames| A comma separated list of bot names. The bot will ignore messages from these users.|
|KeyFile| The location of the .env file for Twitch API credentials. Look below for more information on how to set up the keys.env file.|
|UserScopes| The permissions the chatbot should have.|


### Setup of the .env file

The .env file is used to store the Twitch API credentials and other sensitive information. The bot uses the `python-dotenv` library to load the variables from the .env file. The .env file should be where the "KeyFile" setting in the config points to and should have the following format:
| Variable | Description |
|----------|-------------|
|APP_ID| The Client ID of your Twitch application. You can find this in the Twitch Developer Console.|
|APP_SECRET| The Client Secret of your Twitch application. You can find this in the Twitch Developer Console.|
|BROADCASTER_ID| The ID of the broadcaster (the Twitch channel) the bot is running in. You can get this by using the TwitchBroadcasterID.py file in the tools folder|
|TOKEN| The access token for the Twitch API. You can generate this using the Twitch API and the Client ID and Client Secret of your application. Make sure to include the necessary scopes for the bot to function properly.|
|BOTNAME| The name of the bot. This is used for the IRC connection to Twitch chat.|

  
  
  ```
    APP_ID=your_client_id
    APP_SECRET=your_client_secret
    BROADCASTER_ID=your_broadcaster_id
    TOKEN=your_twitch_token
    YTMD_TOKEN=your_ytmd_token [only needed if you want to use the music features of the bot]:#
   ```