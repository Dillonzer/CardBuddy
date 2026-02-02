
from cards import Cards
from sets import Sets
from consts import Consts
from postgres import PostgresDB

class CardBuddy():
    def __init__(self):
        self.token = Consts.TOKEN
        self.botId = Consts.BOT_ID
        self.uri = Consts.URI

        self.cardDict = {}
        self.cardDict[Consts.EN_US] = Cards(self.uri, Consts.EN_US)
       #self.cardDict[Consts.DE_DE] = Cards(self.uri, Consts.DE_DE)
       #self.cardDict[Consts.ES_ES] = Cards(self.uri, Consts.ES_ES)
       #self.cardDict[Consts.FR_FR] = Cards(self.uri, Consts.FR_FR)
       #self.cardDict[Consts.IT_IT] = Cards(self.uri, Consts.IT_IT)
       #self.cardDict[Consts.PT_BR] = Cards(self.uri, Consts.PT_BR)  

        self.setDict = Sets(self.uri)

        if(Consts.ENV != 'development'):
            self.database = PostgresDB()
    