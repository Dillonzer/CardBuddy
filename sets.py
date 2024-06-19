import requests
import json
from collections import Counter
from helper import HelperFunctions

class Sets:
    def __init__(self, uri):
        self.Refresh(uri)

    def Refresh(self, uri):
        self.sets = []
        self.uniqueNames = []
        self.autocompleteNames = []        
        try:            
            print("Getting Sets...")
            url = "https://raw.githubusercontent.com/Dillonzer/dillonzer.github.io/master/data/sets.json"
            response = requests.request("GET", url)
            jsonSets = json.loads(response.text.encode('utf8'))
            
            self.sets = jsonSets
            self.uniqueNames = self.GetUniqueNames()   
            self.autocompleteNames = self.GetAutocompleteNames()         
            print("Gathered Sets!")
        except Exception as e:
            self.sets = []
            print(f"Failed to get Sets! Exception: {e}")
    
    def GetUniqueNames(self):
        uniqueNames = []
        for val in self.sets:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"].lower()) 
        
        return uniqueNames

    def GetAutocompleteNames(self):
        uniqueNames = []
        for val in self.sets:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"]) 
        
        return uniqueNames

    def S(self, word):
        names = Counter(self.uniqueNames)
        N=sum(names.values())
        return names[word] / N

    def setCorrection(self, word): 
        return max(self.setCandidates(word), key=self.S)

    def setKnown(self, words): 
        return set(w for w in words if w in self.uniqueNames)

    def setCandidates(self, word): 
        return (self.setKnown([word]) or self.setKnown(HelperFunctions.edits1(word)) or self.setKnown(HelperFunctions.edits2(word)) or [word])
