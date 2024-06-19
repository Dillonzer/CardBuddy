from consts import Consts
from helper import HelperFunctions

class EnergyType:
    @staticmethod
    def GetEnergyTypeImage(card):
        if (card["type"].lower() == "Colorless".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/colorless.png"
        if (card["type"].lower() == "Colorless,Psychic".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/colorlessPsychic.png"
        if (card["type"].lower() == "Dark".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/darkness.png"
        if (card["type"].lower() == "Dark,Psychic".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/darkPsychic.png"
        if (card["type"].lower() == "Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/darkness.png"
        if (card["type"].lower() == "Darkness,Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/darkMetal.png"
        if (card["type"].lower() == "Dragon".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/dragon.png"
        if ("energy" in card["type"].lower()):
            if("Darkness Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/darkness.png"
            if("Water Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/water.png"
            if("Psychic Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/psychic.png"
            if("Metal Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/metal.png"
            if("Lightning Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/lightning.png"
            if("Grass Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/grass.png"
            if("Fire Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fire.png"
            if("Fighting Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fightning.png"
            if("Fairy Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fairy.png"
            if("Dragon Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/dragon.png"
            if("Colorless Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/colorless.png"      
            if("Energy FDY" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fightingDarkFairy.png"
            if("Energy GRW" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/grassFireWater.png"
            if("Energy LPM" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/lightningPsychicMetal.png"
            if("Energy GRPD" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/blend_1.png"
            if("Energy WLFM" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/blend_2.png"
            if("Rainbow Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/rainbow.png"
            if("Aurora Energy" in card["name"]):
                return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/rainbow_2.png"
        if (card["type"].lower() == "Fairy".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fairy.png"
        if (card["type"].lower() == "Fighting".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fighting.png"
        if (card["type"].lower() == "Fighting,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fightDark.png"
        if (card["type"].lower() == "Fire".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fire.png"
        if (card["type"].lower() == "Fire,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fireDark.png"
        if (card["type"].lower() == "Fire,Lightning".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fireLightning.png"
        if (card["type"].lower() == "Fire,Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/fireMetal.png"
        if (card["type"].lower() == "Grass".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/grass.png"
        if (card["type"].lower() == "Grass,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/grassDark.png"
        if (card["type"].lower() == "Grass,Lightning".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/grassLightning.png"
        if (card["type"].lower() == "Grass,Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/grassMetal.png"
        if (card["type"].lower() == "Lightning".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/lightning.png"
        if (card["type"].lower() == "Lightning,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/lightningDarkness.png"
        if (card["type"].lower() == "Lightning,Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/lightningMetal.png"
        if (card["type"].lower() == "Lightning,Water".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/lightningWater.png"
        if (card["type"].lower() == "Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/metal.png"
        if (card["type"].lower() == "Metal,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/metalDark.png"
        if (card["type"].lower() == "Psychic".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/psychic.png"
        if (card["type"].lower() == "Psychic,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/psychicDark.png"
        if (card["type"].lower() == "Psychic,Fairy".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/psychicFairy.png"
        if (card["type"].lower() == "Psychic,Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/psychicMetal.png"
        if (card["type"].lower() == "Trainer".lower()):
            return None
        if (card["type"].lower() == "Trainer:Item".lower()):
            return None
        if (card["type"].lower() == "Trainer:Item:Pokémon Tool".lower()):
            return None
        if (card["type"].lower() == "Trainer:Item:Pokémon Tool F".lower()):
            return None
        if (card["type"].lower() == "Trainer:Stadium".lower()):
            return None
        if (card["type"].lower() == "Trainer:Supporter".lower()):
            return None
        if (card["type"].lower() == "Water".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/water.png"
        if (card["type"].lower() == "Water,Darkness".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/waterDark.png"
        if (card["type"].lower() == "Water,Fairy".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/waterFairy.png"
        if (card["type"].lower() == "Water,Fighting".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/waterFighting.png"
        if (card["type"].lower() == "Water,Metal".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/waterMetal.png"
        if (card["type"].lower() == "Water,Fire".lower()):
            return "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/waterFire.png"
        
        return None


       