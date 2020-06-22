import logging
import yaml
import time
import json
import re
import os
import requests
import spotipy

LOGGER = logging.getLogger(__name__)
username = 'peloso'
spotify_app_info_file = 'spotify.yml'
users_file = 'users_db'

def read_info_file():
    # Read spotify info file
    spotify_app_dir = os.path.abspath('spotipy')
    path = os.path.join(spotify_app_dir, spotify_app_info_file)
    with open(path, 'r') as handle:
        spotify_info = yaml.safe_load(handle)
    return spotify_info

def jprint(text):
    print(json.dumps(text, indent=4))

def _add_custom_values_to_token_info(token_info):
        """
        Store some values that aren't directly provided by a Web API
        response.
        """
        token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
        return token_info

def _save_token_info(token_info, cache_path):
    if cache_path:
        try:
            f = open(cache_path, "w")
            f.write(json.dumps(token_info))
            f.close()
        except IOError:
            LOGGER.warning('Couldn\'t write token to cache at: %s', cache_path)

def _associate_users(wt_person_email, spotify_username = None):
    with open(users_file, "r") as file:
        content = file.read()
        if content:
            db = json.loads(content)
        else:
            db = {}
    if wt_person_email in db:
        if spotify_username and db[wt_person_email] != spotify_username:
            db[wt_person_email] = spotify_username
            with open(users_file, "w") as file:
                file.write(json.dumps(db))
        else:
            return db[wt_person_email]
    elif spotify_username:
        db[wt_person_email] = spotify_username
        with open(users_file, "w") as file:
            file.write(json.dumps(db))
        return spotify_username
    else:
        return None

def get_user_token_or_auth_url(username, oauth_manager=None):
    spotify_info = read_info_file()
    sp_oauth = oauth_manager or spotipy.SpotifyOAuth(
        client_id = spotify_info.get('client_id'),
        client_secret = spotify_info.get('client_secret'),
        redirect_uri = spotify_info.get('redirect_uri'),
        scope = spotify_info.get('scope'),
        cache_path = spotify_info.get('cache_path').format(username),
        username=username
    )
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return sp_oauth.get_authorize_url()
    else:
        return token_info["access_token"]

def get_token_from_code(code):
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    spotify_info = read_info_file()
    # Prepare POST message to get the access token from the code
    payload = {
        "client_id": spotify_info.get('client_id'),
        "client_secret": spotify_info.get('client_secret'),
        "redirect_uri": spotify_info.get('redirect_uri'),
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(url = OAUTH_TOKEN_URL, data = payload)
    if response.status_code != 200:
        raise Exception(response.reason)
    token_info = response.json()
    token_info = _add_custom_values_to_token_info(token_info)
    #print(token_info)
    me = get_my_info(token_info["access_token"])
    _save_token_info(token_info, spotify_info.get('cache_path').format(me['id']))
    return token_info["access_token"]

def get_my_info(token):
    spoty = spotipy.Spotify(auth = token)
    return spoty.me()

def spotify_message(command, person_email = None):
    commands = re.split(r'\s+', command)
    if len(commands) > 1:
        if commands[1] == "auth":
            if len(commands) > 2:
                username = commands[2]
                token = get_user_token_or_auth_url(username)
                if 'http' in token:
                    return f'User <{username}>, please go to the following url to authenticate and try again this command later: {token}'
                elif token:
                    # Associate person_email with spotify username
                    response = _associate_users(person_email, username)
                    if response:
                        return f'User "{username}" correctly authenticated'
                    else:
                        return 'Error while saving the user'
                else:
                    return 'There was an error'
            else:
                return 'A spotify username is required after "auth"'
        elif commands[1] == "status":
            username = _associate_users(person_email)
            if username:
                token = get_user_token_or_auth_url(username)
                if 'http' in token:
                    return f'User {username} not authenticated. Please run "spotify auth {username}"' 
                else:
                    me = get_my_info(token)
                    product = me.get('product', '')
                    if product:
                        return f'User "{username}" ({product}) is active'
                    else:
                        return f'Something is wrong with {username}'
                    return json.dumps(get_my_info(token), indent=4)
            else:
                return f'User {person_email} not registered. Please run "spotify auth [spotify_username]"'
    else:
        return 'Valid options for spotify: auth, status'

def main():
    result = get_user_token_or_auth_url(username = username)
    print(result)

if __name__ == "__main__":
    main()