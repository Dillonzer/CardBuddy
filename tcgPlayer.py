import requests
import aiohttp
import json
import re
from consts import Consts
from datetime import datetime

class TCGPlayer:    
    def __init__(self):
        self.GetTCGPlayerAuth()

    def GetTCGPlayerAuth(self):
        try:
            print("Getting TCGPlayer Auth...")
            authUrl = "https://api.tcgplayer.com/token"
            authPayload = f"grant_type=client_credentials&client_id={Consts.TCGPLAYER_CLIENT_ID}&client_secret={Consts.TCGPLAYER_CLIENT_SECRET}"
            authHeaders = {
            'Content-Type': 'text/plain',
            }
            authResponse = requests.request("POST", authUrl, headers=authHeaders, data = authPayload)
            jsonAuth = json.loads(authResponse.text.encode('utf8'))
            
            self.AccessToken = jsonAuth['access_token']      
            self.Expires =  datetime.strptime(jsonAuth['.expires'], '%a, %d %b %Y %H:%M:%S %Z')
            print("TCGPlayer Auth Grabbed!")            
        except Exception as e:
            print(f"Failed to hit TCGPlayer due to {e}.")

    async def GetTCGPlayerMarketPrice(self, id, cardLink):
        try:  
            if(self.AccessToken == None):
                return Consts.COULD_NOT_FIND_PRICES
            elif(datetime.now() >= self.Expires):
                self.GetTCGPlayerAuth()

            url = "https://api.tcgplayer.com/v1.39.0/pricing/product/"+id

            payload = {}
            headers = {
            'Authorization': 'Bearer '+self.AccessToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:        
                    jsonMarketPrice = await response.json()
                    tcgPriceReturnValue = ""
                    normalPriceFound = False
                    holoPriceFound = False
                    reverseHoloPriceFound = False

                    if(jsonMarketPrice['success'] == False):
                        return Consts.COULD_NOT_FIND_PRICES

                    for price in jsonMarketPrice['results']:                
                        if price['subTypeName'] == "Holofoil":
                            if price['marketPrice'] is not None:                                
                                if holoPriceFound or normalPriceFound or reverseHoloPriceFound:
                                    tcgPriceReturnValue += " | "
                                tcgPriceReturnValue += "Holo: [$"+str("{:.2f}".format(price['marketPrice']))+"]("+cardLink+")"
                                holoPriceFound = True                            

                        if price['subTypeName'] == "Reverse Holofoil":
                            if price['marketPrice'] is not None:                      
                                if holoPriceFound or normalPriceFound or reverseHoloPriceFound:
                                    tcgPriceReturnValue += " | "
                                tcgPriceReturnValue += "Reverse Holo: [$"+str("{:.2f}".format(price['marketPrice']))+"]("+cardLink+")"
                                reverseHoloPriceFound = True
                        
                        if price['subTypeName'] == "Normal":
                            if price['marketPrice'] is not None:                      
                                if holoPriceFound or normalPriceFound or reverseHoloPriceFound:
                                    tcgPriceReturnValue += " | "
                                tcgPriceReturnValue += "Non Holo: [$"+str("{:.2f}".format(price['marketPrice']))+"]("+cardLink+")"
                                normalPriceFound = True

                    if holoPriceFound or normalPriceFound or reverseHoloPriceFound:
                        return tcgPriceReturnValue
                    else:
                        return Consts.COULD_NOT_FIND_PRICES
        except Exception as e:
            print(f"Failed to hit TCGPlayer due to {e}.")
            return Consts.COULD_NOT_FIND_PRICES 
            
        return Consts.COULD_NOT_FIND_PRICES 
