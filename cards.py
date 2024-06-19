import requests
import json
import re
from collections import Counter
from helper import HelperFunctions

class Cards:
    def __init__(self, uri, locale):
        self.Refresh(uri, locale)
    
    def GetUniqueNames(self):
        uniqueNames = []
        for val in self.cards:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"].lower()) 
        
        return uniqueNames
    
    def GetAutocompleteNames(self):
        uniqueNames = []
        for val in self.cards:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"]) 
        
        return uniqueNames

    def Refresh(self, uri, locale):
        self.card = []
        self.uniqueNames = []
        self.autocompleteNames = []
        try:
            print(f"Getting Cards for {locale}...")
            url = "https://raw.githubusercontent.com/Dillonzer/dillonzer.github.io/master/data/cards.json"
            response = requests.request("GET", url)
            jsonCards = json.loads(response.text.encode('utf8'))
            
            self.cards = jsonCards
            self.uniqueNames = self.GetUniqueNames()
            self.autocompleteNames = self.GetAutocompleteNames()
            print(f"Gathered Cards for {locale}!")
        except Exception as e:
            self.cards = []
            print(f"Failed to get Cards for {locale}! Exception: {e}")
    
    @staticmethod
    def GetCardNumber(card):
        number = re.sub(r'[a-z]+', '', card['number'], re.I)
        try:
            number = int(number)
            return int(number)
        except ValueError:
            return 0

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
