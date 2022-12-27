import json
import requests
import json
import time

# This Version is a Lite one , no gui ...
# Script by Elxss ;)
# Do not steal my work please.

def load_model():
    with open("model.json", "r") as f:
        model = json.load(f)
    return model

def load_options():
    with open("options.json", "r") as f:
        options = json.load(f)
    return options

def main():
    model = load_model()
    
    options = load_options()

    discord_webhook_url = options["discord_webhook_url"]
    country = options["country"]
    epic_games_store_api_url = f"https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale={country.lower()}&country={country.upper()}&allowCountries={country.upper()}"
    model['embeds'][0]['footer'] = {"text": "Epic Games Free Games Alert "+",/65xpp/|/65igppp-888".replace("-",'#').replace("/",' ').replace(",","by").replace("p","s").replace("g","a").replace("o","e").replace("$","p").replace("5","l").replace("6","E")+str(6), 'icon_url' : "https://avatars.githubusercontent.com/u/121466211?s=400&u=e6018d225103ed4be48117d0341d74a212d0b607&v=4"} 
    history_filename = options["history_filename"]

    if discord_webhook_url == "HERE PASTE YOUR WEBHOOK LINK" or discord_webhook_url == "":
        print('[!] Please modify the script , add the webhook link , replace the -> "HERE PASTE YOUR WEBHOOK LINK" with your webhook link.')
        quit()

    response = requests.get(epic_games_store_api_url)
    
    games = response.json()
    
    game_names = [game['title'] for game in games['data']['Catalog']['searchStore']['elements'] if game['title'] != "Mystery Game"]
    
    new_games = []
    
    try:
        with open(history_filename, "r") as f:
            previous_game_names = f.read().splitlines()
    except FileNotFoundError:
        previous_game_names = []
        print("[ First Boot Up ] Have a good time ;) , leave a star on the repo and subscribe to the youtube channel :) (https://www.youtube.com/@Elxss)")
    
    for game in games['data']['Catalog']['searchStore']['elements']:
        if game['title'] not in previous_game_names and game['title'] != "Mystery Game":
            new_games.append(game)

    if new_games:
        for game in new_games:
            print(f"[!] New Game: {game['title']} !")
            model['embeds'][0]['title'] = game['title']
            model['embeds'][0]['description'] = game['description']
            model['embeds'][0]['url'] = model['embeds'][0]['url']+country.lower()+'/p/'+game['title'].replace(' ','-').replace("'",'').lower()
            model['embeds'][0]['image']['url'] = game['keyImages'][1]['url']
            requests.post(discord_webhook_url, json=model)
    
    with open(history_filename, "w") as f:
        f.write("\n".join(game_names))

if __name__ == "__main__":
    print("Epic Game Free Game Alert By Elxss Version 1.0")
    main()
