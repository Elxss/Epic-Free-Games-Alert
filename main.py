import json
import requests
import json

# Script by Elxss ;)

def load_options():
    with open("options.json", "r") as f:
        options = json.load(f)
    return options

def main():
    options = load_options()

    discord_webhook_url = options["discord_webhook_url"]
    country = options["country"]
    epic_games_store_api_url = f"https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale={country.lower()}&country={country.upper()}&allowCountries={country.upper()}"
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
    
    for game in games['data']['Catalog']['searchStore']['elements']:
        if game['title'] not in previous_game_names and game['title'] != "Mystery Game":
            new_games.append(game)
    
    if new_games:
        for game in new_games:
            print(f"New Game: {game['title']} !")
            message = f"Nouveau jeu gratuit disponible sur l'Epic Games Store : {game['title']}\nImage : {game['keyImages'][1]['url']} \ndescription : {game['description']}"
            payload = {"content": message}
            requests.post(discord_webhook_url, json=payload)
    
    with open(history_filename, "w") as f:
        f.write("\n".join(game_names))

if __name__ == "__main__":
    print("This is a beta release ;)")
    main()