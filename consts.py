from os import environ

class Consts:    
    BOT_PREFIX = environ.get('BOT_PREFIX')
    BOT_ID = environ.get('BOT_ID')
    TOKEN = environ.get('TOKEN')
    URI = environ.get('URI')
    DM_MESSAGE = "I have direct messaged you!"
    ONLY_REQUESTER_CAN_CYCLE_MESSAGE = "Only the original requester may cycle through the cards. Sorry about the inconvenience."
    LOGO_ADDRESS = "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/Logo.png"
    POKEMON_CARD_LOGO_ADDRESS = "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/TCG_Logo.png"
    SAD_FACE = "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/ptcgo_cry.png"
    EN_US = "en_US"
    DE_DE = "de_DE"
    ES_ES = "es_ES"
    FR_FR = "fr_FR"
    IT_IT = "it_IT"
    PT_BR = "pt_BR"
    SPELL_CHECK_TIME = 2
    TOPGG_AUTHTOKEN = environ.get('TOPGG_AUTHTOKEN')
    TCGPLAYER_CLIENT_ID = environ.get('TCGPLAYER_CLIENT_ID')
    TCGPLAYER_CLIENT_SECRET = environ.get('TCGPLAYER_CLIENT_SECRET')
    DATABASE_URL = environ.get('DATABASE_URL')
    COULD_NOT_FIND_PRICES = "Could not find Prices"
    POKEAPI_URL = "https://img.pokemondb.net/sprites/sword-shield/normal"
    POKETRAINER_URL = "https://pokeapi.co/api/v2/item"
    PLAYLIMITLESSTCG_API = "https://play.limitlesstcg.com/ext/live"
    PLAYLIMITLESSTCG_URL = "https://play.limitlesstcg.com/tournament"
    COULD_NOT_FIND_TOURNAMENT = "Error pulling tournaments"
    PLAYLIMITLESSTCG_LOGO = "https://play.limitlesstcg.com/limitless.png"
    TCGDEX_LOGO = "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/!Logos/tcgdex_logo.png"
    ENV = "prod"