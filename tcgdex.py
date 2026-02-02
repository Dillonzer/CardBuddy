import requests
import json
from collections import Counter
from helper import HelperFunctions

class PokemonPocket:
    def __init__(self):
        self.Refresh()
    
    def GetUniqueNamesCards(self):
        uniqueNames = []
        for val in self.cards:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"].lower()) 
        
        return uniqueNames
    
    def GetAutocompleteNamesCards(self):
        uniqueNames = []
        for val in self.cards:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"]) 
        
        return uniqueNames
    
    def GetUniqueNamesSets(self):
        uniqueNames = []
        for val in self.sets:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"].lower()) 
        
        return uniqueNames
    
    def GetAutocompleteNamesSets(self):
        uniqueNames = []
        for val in self.sets:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"]) 
        
        return uniqueNames

    def Refresh(self):
        self.cards = []
        self.sets = []
        self.uniqueNamesCards = []
        self.autocompleteNamesCards = []
        self.uniqueNamesSets = []
        self.autocompleteNamesSets = []
        try:
            print(f"Getting Pokemon Pocket Cards")
            sets = self.getAllSets();
            for set in sets["sets"]:
                self.sets.append(set)
                setCards = self.getCardsInSet(set["name"])
                for card in setCards["cards"]:
                    self.cards.append(card)
            
            self.uniqueNamesCards = self.GetUniqueNamesCards()
            self.autocompleteNamesCards = self.GetAutocompleteNamesCards()
            self.uniqueNamesSets = self.GetUniqueNamesSets()
            self.autocompleteNamesSets = self.GetAutocompleteNamesSets()
            print(f"Gathered Pokemon Pocket!")
        except Exception as e:
            self.cards = []
            self.sets = []
            print(f"Failed to get Pokemon Pocket Cards! Exception: {e}")

    def C(self, word): 
        names = Counter(self.uniqueNames)
        N = sum(names.values())
        return names[word] / N

    def cardCorrection(self, word): 
        return max(self.cardCandidates(word), key=self.C)

    def cardKnown(self, words): 
        return set(w for w in words if w in self.uniqueNames)
    
    def cardCandidates(self, word): 
        return (self.cardKnown([word]) or self.cardKnown(HelperFunctions.edits1(word)) or self.cardKnown(HelperFunctions.edits2(word)) or [word])

    @staticmethod
    def getAllSets():
        try:
            url = f"https://api.tcgdex.net/v2/en/series/tcgp"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit TCGDex due to {e}.")
            return None
        
    
    @staticmethod
    def getCardsInSet(setName):
        try:
            url = f"https://api.tcgdex.net/v2/en/sets/{setName}"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit TCGDex due to {e}.")
            return None
        

    @staticmethod
    def GetSpecificCard(cardId):
        try:
            url = f"https://api.tcgdex.net/v2/en/cards/{cardId}"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit TCGDex due to {e}.")
            return None
    
    def GetSetFromCard(self, card):
        replaceValue = "-"+card["localId"]
        setId = card["id"].replace(replaceValue,"")
        for s in self.sets:
            if s["id"] == setId:
                return s
        return None