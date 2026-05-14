import requests

url = "https://api.twitch.tv/helix/users"
client_id = "" # Your Twitch application's Client ID
access_token = "" # Your Twitch API access token with the necessary scopes to access user information. NEVER SHARE THIS WITH ANYONE. 
username = "" # The Twitch username of the broadcaster (the Twitch channel) the bot is running in.

def get_broadcaster_id(username, client_id, access_token):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }   

    params = {
        "login": username
    }
    response = requests.get(url, headers=headers, params=params)
    print(response.json())
    
get_broadcaster_id(username, client_id, access_token)