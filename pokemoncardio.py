import requests
import json
import time

class PokemonCardIO:
    @staticmethod
    def GetDeck(cardName, format):
        try:
            url = f"https://pokemoncard.io/api-public/getDeck.php?name={cardName}&limit=5&format={format}"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit PokemonCard.io due to {e}.")
            return None
    
    @staticmethod
    def GetRandomDeck(format):
        try:
            url = f"https://pokemoncard.io/api-public/getDeck.php?format={format}&sort=random&cache={time.time()}"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit PokemonCard.io due to {e}.")
            return None

