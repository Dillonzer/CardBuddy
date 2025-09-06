import asyncio
import json
import aiohttp
from datetime import datetime
from cards import Cards
from consts import Consts
from helper import HelperFunctions
from tcgPlayer import TCGPlayer
from cardbuddy import CardBuddy
from energyType import EnergyType
from pokemoncardio import PokemonCardIO
import interactions

guild_ids = [642081591371497472]

cardBuddy = CardBuddy()
tcgPlayer = TCGPlayer()

client = interactions.AutoShardedClient(token=Consts.TOKEN)

interactions.const.CLIENT_FEATURE_FLAGS["FOLLOWUP_INTERACTIONS_FOR_IMAGES"] = True

async def BuildEmbed(ctx, val, tcgPlayerPrices, thumbnail):
    e = interactions.Embed()
    e.title= HelperFunctions.GetEmoji(val['name']) + " (" + HelperFunctions.GetEmojiForNumber(str(val['number']).upper()) + ")"
    if(thumbnail is not None):
        e.set_thumbnail(url=thumbnail)
    e.set_image(url=val['imageUrlHiRes'])
    e.color = interactions.BrandColors.GREEN
    e.set_footer(text= val['set']['name'] + " - Released: " + val['set']['releaseDate'],icon_url=val['set']['symbolUrl'])
    if(val['set']['standardLegal'] == True):
        legality = "Standard: <:legal:885930775533461564>"
    else:        
        legality = "Standard: <:banned:885930754842976326>"
    if(val['set']['expandedLegal'] == True):
        legality += " - Expanded: <:legal:885930775533461564>"
    else:        
        legality += " - Expanded: <:banned:885930754842976326>" 
    if(val['set']['glcLegal'] == True):
        legality += " - GLC: <:legal:885930775533461564>"
    else:        
        legality += " - GLC: <:banned:885930754842976326>"       
    #e.add_field(name="Legality",value=legality,inline=False)
    if(cardBuddy.database.GetTCGPlayerSettings(ctx.guild.id) == 0):
        if(tcgPlayerPrices == True):
            marketPrice = await tcgPlayer.GetTCGPlayerMarketPrice(str(val['tcgPlayerCardId']),val['tcgPlayerCardUrl'])
            if(marketPrice != Consts.COULD_NOT_FIND_PRICES):
                e.add_field(name="TCGPlayer Market Prices (:flag_us:)",value=marketPrice,inline=True)
    #if(cardBuddy.database.GetPTCGLPricesSettings(ctx.guild.id) == 0):
        #if(val['craftingCost'] is not None):
            #e.add_field(name="PTCGL Crafting Cost", value = f"{val['craftingCost']} <:CraftingCurrency:946039553708400660>")
    return e

def GetAllCardsForLocale(locale):
    return cardBuddy.cardDict[Consts.EN_US]

def GetLocaleForUser(userId):
    return Consts.EN_US
   
@interactions.slash_command(name="info",
            description="Get information about the bot")
async def PrintCommands(ctx):
    e = interactions.Embed()
    e.color = interactions.BrandColors.GREEN
    e.title = "Information!"
    e.description = "Thanks for using Card Buddy! Visit my [top.gg](https://top.gg/bot/642081991071891469) page! If you'd like to support what I do please follow me on [Patreon](https://www.patreon.com/bePatron?u=34112337)"
    e.set_author(name="Card Buddy",icon_url=Consts.LOGO_ADDRESS)
    e.set_thumbnail(url=Consts.POKEMON_CARD_LOGO_ADDRESS)
    
    commands = "• `/card`: Displays a picture of the card in that set or all cards with that name!\n"
    commands += "• `/card_text`: Displays a picture of the card that contains the text you are searching!\n"
    commands += "• `/what_set_is_this_card_in`: PMs you a list of all the sets that card is in!\n"
    commands += "• `/all_sets`: PMs you a list of all sets with set codes!\n"
    commands += "• `/set`: Prints out information about the set you are asking about!\n"
    commands += "• `/set_checklist`: DMs you a Checklist for the set you asked for\n"
    commands += "• `/set_list`: Displays all card in that set! (TCGPlayer Integration disabled for this command)\n"

    adminCommands = "• `/tcgplayer_toggle`: Toggles the TCGPlayer Integration!\n"
    adminCommands += "• `/ptcgl_crafting_toggle`: Toggles the PTCGL Crafting Price Functionality!\n"

    pokemonCardsioCommands = "• `/get_deck`: Get deck information from PokemonCards.io!\n"
    pokemonCardsioCommands += "• `/get_random_deck`: Get a random deck from PokemonCards.io!\n"
    
    e.add_field(name="Commands", value=commands, inline=False)
    e.add_field(name="PokemonCards.io Commands", value=pokemonCardsioCommands, inline=False)
    e.add_field(name="Admin Commands", value=adminCommands, inline=False)
    e.set_footer(text="Created by Dillonzer")

    await ctx.send(embeds = e, ephemeral=True)

@interactions.slash_command(name='tcgplayer_toggle',
        description="Toggles the TCGPlayer Functionality",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
        options=[
            interactions.SlashCommandOption(
                name="toggle",
                description="Toggle the TCGPlayer Prices on the Cards",
                type=interactions.OptionType.STRING,
                required=True,
                choices=[
                    interactions.SlashCommandChoice(
                        name="On",
                        value="on"
                    ),
                    interactions.SlashCommandChoice(
                        name="Off",
                        value="off"
                    )]
            )
        ])
async def ToggleTCGPlayer(ctx, toggle):
    server = ctx.guild.id

    if toggle.lower() == "on":  
        didItWork = cardBuddy.database.DeleteTCGPlayerSettings(server)
        if didItWork:
            msg = f"I've turned on the TCGPlayer integration for {ctx.guild}."

    if toggle.lower() == "off":      
        didItWork = cardBuddy.database.InsertTCGPlayerSettings(server)    
        if didItWork:            
            msg = f"I've turned off the TCGPlayer integration for {ctx.guild}."            

    if(toggle.lower() != "on" and toggle.lower() != "off"):
        msg = "Please either use on or off for this command to work."        
    
    await ctx.send(msg, ephemeral=True)

@interactions.slash_command(name='ptcgl_crafting_toggle',
        description="Toggles the PTCGL Crafting Price Functionality",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
        options=[
            interactions.SlashCommandOption(
                name="toggle",
                description="Toggle the prices of PTCGL Crafting Price",
                type=interactions.OptionType.STRING,
                required=True,
                choices=[
                    interactions.SlashCommandChoice(
                        name="On",
                        value="on"
                    ),
                    interactions.SlashCommandChoice(
                        name="Off",
                        value="off"
                    )]
            )
        ])
async def TogglePTCGLPrices(ctx, toggle):
    server = ctx.guild.id

    if toggle.lower() == "on":
        didItWork = cardBuddy.database.DeletePTCGLPricesSettings(server)
        if didItWork:
            msg = f"I've turned on the PTCGL Crafting Price for {ctx.guild}."

    if toggle.lower() == "off":
        didItWork = cardBuddy.database.InsertPTCGLPricesSettings(server)
        if didItWork:
            msg = f"I've turned off the PTCGL Crafting Price for {ctx.guild}."            
    
    if(toggle.lower() != "on" and toggle.lower() != "off"):
        msg = "Please either use on or off for this command to work."        

    await ctx.send(msg, ephemeral=True)

@interactions.slash_command(name='set',
        description="Shows specific set",
        options=[
            interactions.SlashCommandOption(
                name="name",
                description="Name of the set. Could be the PTCGO code, set abbreviation, or full set name",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ])
async def GetSpecificSet(ctx, name):
    await ctx.defer()
    e = interactions.Embed()
    e.color = interactions.BrandColors.GREEN
    autoFillSuggest = False
    name = HelperFunctions.ReplaceCharacters(name)
        
    message = ""
    suggestions = "Could not find `" + name + "`.\n"

    suggestionArray = []
    foundSet = False
    for val in cardBuddy.setDict.sets:
        if val['name'].lower() == name.lower():
            e.title = val['name']
            if(val['standardLegal'] == True):
                standardLegality = "<:legal:885930775533461564>"
            else:        
                standardLegality = "<:banned:885930754842976326>"
            if(val['expandedLegal'] == True):
                expandedLegality = "<:legal:885930775533461564>"
            else:        
                expandedLegality = "<:banned:885930754842976326>"
            if(val['glcLegal'] == True):
                glcLegality = "<:legal:885930775533461564>"
            else:        
                glcLegality = "<:banned:885930754842976326>"        
            message = "SetCode: " + val['code'] + "\nSeries: " + val['series'] + "\nPTCGO Code: " + str(val['ptcgoCode']) + "\nStandard Legal: "  + standardLegality + "\nExpanded Legal: " + expandedLegality +"\nGLC Legal: " + glcLegality + "\nTotal Cards: " + str(val['totalCards']) + "\nRelease Date: " + val['releaseDate']
            e.set_image(url=val['logoUrl'])
            e.set_thumbnail(url=val['symbolUrl'])
            foundSet = True
        else:
            if (name.lower() in val['name'].lower() and len(name) > 3):
                if (val['name'] not in suggestionArray):
                    if(autoFillSuggest is False):
                        suggestions += "Attempted Suggestions:\n"
                        autoFillSuggest = True
                    suggestionArray.append(val['name'])
                    suggestions += "`" + val['name'] + "`\n"   

    if not foundSet:
        for val in cardBuddy.setDict.sets:
            if val['code'].lower() == name.lower():
                e.title = val['name']
                if(val['standardLegal'] == True):
                    standardLegality = "<:legal:885930775533461564>"
                else:        
                    standardLegality = "<:banned:885930754842976326>"
                if(val['expandedLegal'] == True):
                    expandedLegality = "<:legal:885930775533461564>"
                else:        
                    expandedLegality = "<:banned:885930754842976326>"
                if(val['glcLegal'] == True):
                    glcLegality = "<:legal:885930775533461564>"
                else:        
                    glcLegality = "<:banned:885930754842976326>"     
                message = "SetCode: " + val['code'] + "\nSeries: " + val['series'] + "\nPTCGO Code: " + str(val['ptcgoCode']) + "\nStandard Legal: "  + standardLegality + "\nExpanded Legal: " + expandedLegality + "\nGLC Legal: " + glcLegality + "\nTotal Cards: " + str(val['totalCards']) + "\nRelease Date: " + val['releaseDate']
                e.set_image(url=val['logoUrl'])
                e.set_thumbnail(url=val['symbolUrl'])
                foundSet = True             

    if not foundSet:
        for val in cardBuddy.setDict.sets:
            if str(val['ptcgoCode']).lower() == name.lower():
                e.title = val['name']
                if(val['standardLegal'] == True):
                    standardLegality = "<:legal:885930775533461564>"
                else:        
                    standardLegality = "<:banned:885930754842976326>"
                if(val['expandedLegal'] == True):
                    expandedLegality = "<:legal:885930775533461564>"
                else:        
                    expandedLegality = "<:banned:885930754842976326>"
                if(val['glcLegal'] == True):
                    glcLegality = "<:legal:885930775533461564>"
                else:        
                    glcLegality = "<:banned:885930754842976326>"     
                message = "SetCode: " + val['code'] + "\nSeries: " + val['series'] + "\nPTCGO Code: " + str(val['ptcgoCode']) + "\nStandard Legal: "  + standardLegality + "\nExpanded Legal: " + expandedLegality + "\nGLC Legal: " + glcLegality + "\nTotal Cards: " + str(val['totalCards']) + "\nRelease Date: " + val['releaseDate']
                e.set_image(url=val['logoUrl'])
                e.set_thumbnail(url=val['symbolUrl'])
                foundSet = True
            
    if not foundSet:
        message = suggestions
        e.title= "Whoa! I can't find that set!"
        e.color = interactions.BrandColors.RED
        e.set_thumbnail(url = Consts.SAD_FACE)
    
    e.description = message

    await ctx.send(embeds = e)

@GetSpecificSet.autocomplete("name")
async def autocomplete_set(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.setDict.autocompleteNames if ctx.kwargs['name'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)
    except:
        pass

@interactions.slash_command(name='all_sets',
        description="DMs you all the sets in the game")
async def GetAllSets(ctx):   
    await ctx.defer(ephemeral=True)
    message = ""
    count = 0
    user = ctx.author
    for val in cardBuddy.setDict.sets:
        message += val['name'] + " - PTCGO Code: " + str(val['ptcgoCode']) + " - SetCode: " + val['code'] + "\n"
        count = count + 1

        if count == 10:
            await user.send(message)
            message = ""
            count = 0
    
    if (message != ""):
        await user.send(message)
        
    await ctx.send(Consts.DM_MESSAGE, ephemeral=True)

@interactions.slash_command(name='card',
        description="Shows the specific card",
        options=[
            interactions.SlashCommandOption(
                name="name",
                description="Name of the card",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            ),     
            interactions.SlashCommandOption(
                name="set",
                description="Name of the set",
                type=interactions.OptionType.STRING,
                required=False,
                autocomplete=True
            ),  
            interactions.SlashCommandOption(
                name="format",
                description="Check just a specific format",
                type=interactions.OptionType.STRING,
                required=False,                
                choices=[
                    interactions.SlashCommandChoice(
                        name="Standard",
                        value="standard"
                    ),
                    interactions.SlashCommandChoice(
                        name="Expanded",
                        value="expanded"
                    ),
                    interactions.SlashCommandChoice(
                        name="GLC",
                        value="glc"
                    )]
            )]
        )
async def GetSpecificCard(ctx, name, set = "", format = ""):
    await ctx.defer()
    user = ctx.author
    userId = ctx.author.id
    count = 0
    locale = GetLocaleForUser(userId)
    ALLCARDS = GetAllCardsForLocale(locale)    
    name = HelperFunctions.ReplaceCharacters(name)
    if(set and format == ""):
        suggestions = f"Could not find `{set} {name}`\n"
    elif(set and format):
        suggestions = f"Could not find `{set} {name} in {format}`\n"
    elif(format):
        suggestions = f"Could not find `{name} in {format}`\n"
    else:        
        suggestions = f"Could not find `{name}`\n"
    embeddedArray = []
    suggestionArray = []
    foundCard = False 

    async def ButtonClick(button_ctx: interactions.Button):
        try:
            nonlocal count
            if button_ctx.ctx.custom_id == f"prev{ctx.id}" and button_ctx.ctx.author == user:
                if count - 1 >= 0:                        
                    count = count - 1
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])
                else:
                    count = maxEmbed - 1
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])
            elif button_ctx.ctx.custom_id == f"next{ctx.id}" and button_ctx.ctx.author == user:
                if count + 1 < maxEmbed:
                    count = count + 1
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])
                else:
                    count = 0
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])                        
            else:
                try:                                                    
                    await button_ctx.ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
                except:
                    pass
        except:
            pass

    for val in ALLCARDS.cards:
        if set and format == "":
            if (name.lower() in val['name'].lower() and len(name) > 3 \
            or val['name'].lower() == name.lower() \
            or val['name'].lower() == name.lower()) \
            and val['set']['name'].lower() == set.lower():
                thumbnail = EnergyType.GetEnergyTypeImage(val)  
                e = await BuildEmbed(ctx,val,True,thumbnail)
                embeddedArray.append(e)
                foundCard = True
        elif set and format:
            if (name.lower() in val['name'].lower() and len(name) > 3 \
            or val['name'].lower() == name.lower() \
            or val['name'].lower() == name.lower()) \
            and val['set']['name'].lower() == set.lower() \
            and val['set'][f"{format}Legal"]:
                thumbnail = EnergyType.GetEnergyTypeImage(val)  
                e = await BuildEmbed(ctx,val,True,thumbnail)
                embeddedArray.append(e)
                foundCard = True
        elif format:
            if (name.lower() in val['name'].lower() and len(name) > 3 \
            or val['name'].lower() == name.lower() \
            or val['name'].lower() == name.lower())  \
            and val['set'][f"{format}Legal"]:
                thumbnail = EnergyType.GetEnergyTypeImage(val)  
                e = await BuildEmbed(ctx,val,True,thumbnail)
                embeddedArray.append(e)
                foundCard = True
        else:
            if (name.lower() in val['name'].lower() and len(name) > 3) \
            or val['name'].lower() == name.lower():
                thumbnail = EnergyType.GetEnergyTypeImage(val) 
                e = await BuildEmbed(ctx,val,True,thumbnail)
                embeddedArray.append(e)
                foundCard = True

    if not foundCard:
        e = interactions.Embed()
        e.title= "Whoa! I can't find that card!"
        e.description = suggestions
        e.color = interactions.BrandColors.RED
        e.set_thumbnail(url = Consts.SAD_FACE)
        embeddedArray.append(e)   

    maxEmbed = len(embeddedArray)

    if maxEmbed > 1:  
        descCount = 0
        for es in embeddedArray:
            descCount = descCount + 1
            es.description = "Showing " + str(descCount) + "/" + str(maxEmbed) + ". Traverse the cards with the buttons below."


        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.RED,
                label="Previous",
                custom_id=f"prev{ctx.id}"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.GREEN,
                label="Next",
                custom_id=f"next{ctx.id}"
            )
        ]
        action_row = interactions.ActionRow(*buttons)
        msg = await ctx.send(embeds = embeddedArray[0], components=[action_row])
          
        try:       
            button_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=ButtonClick, timeout=60)  
        except asyncio.TimeoutError:
            action_row.components[0].disabled = True
            action_row.components[1].disabled = True
            await msg.edit(components=action_row)
            pass
            # When it times out, edit the original message and remove the button(s)
            # return await ctx.edit(embeds = embeddedArray[count], components=[]) 
    else:        
        msg = await ctx.send(embeds = embeddedArray[0]) 

@GetSpecificCard.autocomplete("name")
async def autocomplete_cardname(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.cardDict[Consts.EN_US].autocompleteNames if ctx.kwargs['name'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)
    except:
        pass

@GetSpecificCard.autocomplete("set")
async def autocomplete_cardset(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.setDict.autocompleteNames if ctx.kwargs['set'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)
    except:
        pass

@interactions.slash_command(name='what_set_is_this_card_in',
        description="Get a list of all the sets that card is in",
        options=[
            interactions.SlashCommandOption(
                name="name",
                description="Name of the card",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            )]
        )
async def GetCardSets(ctx, name): 
    await ctx.defer(ephemeral=True)
    user = ctx.author
    userId = ctx.author.id
    locale = GetLocaleForUser(userId)
    ALLCARDS = GetAllCardsForLocale(locale)
    message = ""
    count = 0
    foundCard = False
    suggestionArray = []
    suggestions = "Could not find `" + name + "`.\n"
    autoFillSuggest = False
    name = HelperFunctions.ReplaceCharacters(name)

    for val in ALLCARDS.cards:
        if val['name'].lower() == name.lower() \
        or val['name'].lower() == name.replace('e','é').lower() \
        or val['name'].lower() == name.replace('-', ' ').lower() \
        or val['name'].lower() == name.replace(' ', '-').lower() \
        or val['name'].lower() == name.replace(' gx', '-gx').lower() \
        or val['name'].lower() == name.replace(' ex', '-ex').lower():
            foundCard = True
            message += val['name'] + " (" + str(val['number']) + ") "+" - Set: " + val['set']['name'] + "\n"
            count = count + 1            

            if count == 10:
                await user.send(message)
                message = ""
                count = 0            
        else:            
            if (name.lower() in val['name'].lower() and len(name) > 3):
                if (val['name'] not in suggestionArray):
                    if(autoFillSuggest is False):
                        suggestions += "Attempted Suggestions:\n"
                        autoFillSuggest = True
                    suggestionArray.append(val['name'])
                    suggestions += "`" + val['name'] + "`\n"

    if(count < 10 and count > 0):
        await user.send(message)

    if not foundCard:
        await ctx.send(suggestions, ephemeral=True)
    else:
        await ctx.send(Consts.DM_MESSAGE, ephemeral=True)

@GetCardSets.autocomplete("name")
async def autocomplete_cardsetcard(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.cardDict[Consts.EN_US].autocompleteNames if ctx.kwargs['name'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)
    except:
        pass

@interactions.slash_command(name='set_list',
        description="Show all cards in the specific set",
        options=[
            interactions.SlashCommandOption(
                name="name",
                description="Set name, PTCGO abbreviation, or set abbreviation",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            )]
        )
async def GetSetList(ctx, name):
    await ctx.defer()
    user = ctx.author
    userId = ctx.author.id
    count = 0
    locale = GetLocaleForUser(userId)
    ALLCARDS = GetAllCardsForLocale(locale)
    embeddedArray = []
    suggestionArray = []
    cardArray = []
    foundCard = False
    autoFillSuggest = False 
    name = HelperFunctions.ReplaceCharacters(name)
    suggestions = "Could not find `" + name + "`.\n" 

    for val in ALLCARDS.cards:
        if str(val['set']['ptcgoCode']).lower() == name.lower() or val['set']['code'].lower() == name.lower() or val['set']['name'].lower() == name.lower():
            cardArray.append(val)
            foundCard = True
        else:            
            if (name.lower() in val['set']['name'].lower() and len(name) > 3):
                if (val['set']['name'] not in suggestionArray):
                    if(autoFillSuggest is False):
                        suggestions += "Attempted Suggestions:\n"
                        autoFillSuggest = True
                    suggestionArray.append(val['set']['name'])
                    suggestions += "`" + val['set']['name'] + "`\n"
    
    if foundCard:  
        cardArray.sort(key=Cards.GetCardNumber)
        for card in cardArray:
            thumbnail = EnergyType.GetEnergyTypeImage(card) 
            e = await BuildEmbed(ctx,card,False,thumbnail)
            embeddedArray.append(e)
    
    if not foundCard:
        e = interactions.Embed()
        e.title= "Whoa! I can't find that set!"
        e.set_thumbnail(url = Consts.SAD_FACE)
        e.description = suggestions
        e.color = interactions.BrandColors.RED
        embeddedArray.append(e)   

    async def ButtonClick(button_ctx: interactions.ComponentContext):
        try:
            nonlocal count
            if button_ctx.ctx.custom_id == f"prev{ctx.id}" and button_ctx.ctx.author == user:
                if count - 1 >= 0:                        
                    count = count - 1
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])
                else:
                    count = maxEmbed - 1
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])
            elif button_ctx.ctx.custom_id == f"next{ctx.id}" and button_ctx.ctx.author == user:
                if count + 1 < maxEmbed:
                    count = count + 1
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])
                else:
                    count = 0
                    await button_ctx.ctx.edit_origin(embeds = embeddedArray[count])                        
            else:
                try:                                                    
                    await button_ctx.ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
                except:
                    pass
        except:
            pass

    maxEmbed = len(embeddedArray)

    if maxEmbed > 1:  
        descCount = 0
        for es in embeddedArray:
            descCount = descCount + 1
            es.description = "Showing " + str(descCount) + "/" + str(maxEmbed) + ". Traverse the cards with the buttons below."
        
        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.RED,
                label="Previous",
                custom_id=f"prev{ctx.id}"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.GREEN,
                label="Next",
                custom_id=f"next{ctx.id}"
            )
        ]
        action_row = interactions.ActionRow(*buttons)
        msg = await ctx.send(embeds = embeddedArray[0], components=[action_row])
        try:       
            button_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=ButtonClick, timeout=60)  
        except asyncio.TimeoutError:
            action_row.components[0].disabled = True
            action_row.components[1].disabled = True
            await msg.edit(components=action_row)
            # When it times out, edit the original message and remove the button(s)
            # return await ctx.edit(embeds = embeddedArray[count], components=[])
    else:        
        await ctx.send(embeds = embeddedArray[0]) 

@GetSetList.autocomplete("name")
async def autocomplete_setlist(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.setDict.autocompleteNames if ctx.kwargs['name'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)    
    except:
        pass

@interactions.slash_command(name='set_checklist',
        description="Will send you a DM of the Set Checklist",
        options=[
            interactions.SlashCommandOption(
                name="name",
                description="Set name, PTCGO abbreviation, or set abbreviation",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            )])
async def GetSetChecklist(ctx, name):
    await ctx.defer(ephemeral=True)
    user = ctx.author
    userId = ctx.author.id
    locale = GetLocaleForUser(userId)
    ALLCARDS = GetAllCardsForLocale(locale)
    suggestionArray = []
    cardArray = []
    foundCard = False
    autoFillSuggest = False 
    suggestions = "Could not find `" + name + "`.\n" 
    message = ""
    count = 0
    name = HelperFunctions.ReplaceCharacters(name)

    for val in ALLCARDS.cards:
        if str(val['set']['ptcgoCode']).lower() == name.lower() or val['set']['code'].lower() == name.lower() or val['set']['name'].lower() == name.lower():
            cardArray.append(val)
            foundCard = True
        else:            
            if (name.lower() in val['set']['name'].lower() and len(name) > 3):
                if (val['set']['name'] not in suggestionArray):
                    if(autoFillSuggest is False):
                        suggestions += "Attempted Suggestions:\n"
                        autoFillSuggest = True
                    suggestionArray.append(val['set']['name'])
                    suggestions += "`" + val['set']['name'] + "`\n"
    
    if foundCard:  
        cardArray.sort(key=Cards.GetCardNumber)
        for card in cardArray:
            message += card['name'] + " (" + str(card['number']) + ") "+" - Rarity: " + card['rarity'] + "\n"
            count = count + 1            

            if count == 10:
                await user.send(message)
                message = ""
                count = 0

        if(count < 10 and count > 0):
            await user.send(message)

    if not foundCard:
        await ctx.send(suggestions, ephemeral=True)    
    else:            
        await ctx.send(Consts.DM_MESSAGE, ephemeral=True) 

@GetSetChecklist.autocomplete("name")
async def autocomplete_setchecklist(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.setDict.autocompleteNames if ctx.kwargs['name'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)    
    except:
        pass
 
@interactions.slash_command(name='get_deck',
        description="Get a deck from PokemonCard.io",
        options=[
            interactions.SlashCommandOption(
                name="card",
                description="Card Name",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            interactions.SlashCommandOption(
                name="format",
                description="Choose the format",
                type=interactions.OptionType.STRING,
                required=True,
                choices=[
                    interactions.SlashCommandChoice(
                        name="Standard",
                        value="Standard"
                    ),
                    interactions.SlashCommandChoice(
                        name="Expanded",
                        value="Expanded"
                    ),
                    interactions.SlashCommandChoice(
                        name="Unlimited",
                        value="Unlimited"
                    ),
                    interactions.SlashCommandChoice(
                        name="Gym Leader Challenge",
                        value="Gym Leader Challenge"
                    )])])
async def GetDeckFromPokemonCardio(ctx, card, format):
    decks = PokemonCardIO.GetDeck(card, format)
    if(decks == None or len(decks) <= 0):
        ctx.send("Could not find any decks!")
    else:
        e = interactions.Embed()
        e.title= f"Decks from PokemonCard.io"
        e.color = interactions.BrandColors.YELLOW
        e.set_footer(text="Powered by PokemonCard.io",icon_url="https://images.pokemoncard.io/images/assets/cropped-applogo_high-1-192x192.png")
        deckNames = ""
        for deck in decks:
            deckNames += f"[{deck['deck_name']}]({deck['url']}) created by [{deck['deck_uploader']}]({deck['deck_uploader_profile']}) ({deck['deck_views']} :eye:)\n"

        e.add_field(name="Decks",value=deckNames,inline=False)
    
        await ctx.send(embeds = e)

@GetDeckFromPokemonCardio.autocomplete("card")
async def autocomplete_pokemoncardio(ctx):
    try:
        choices = [
        interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.cardDict[Consts.EN_US].autocompleteNames if ctx.kwargs['card'].lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)    
    except:
        pass

@interactions.slash_command(name='get_random_deck',
        description="Get a random deck from PokemonCard.io",
        options=[
            interactions.SlashCommandOption(
                name="format",
                description="Choose the format",
                type=interactions.OptionType.STRING,
                required=True,
                choices=[
                    interactions.SlashCommandChoice(
                        name="Standard",
                        value="Standard"
                    ),
                    interactions.SlashCommandChoice(
                        name="Expanded",
                        value="Expanded"
                    ),
                    interactions.SlashCommandChoice(
                        name="Unlimited",
                        value="Unlimited"
                    ),
                    interactions.SlashCommandChoice(
                        name="Gym Leader Challenge",
                        value="Gym Leader Challenge"
                    )])])
async def GetRandomDeckFromPokemonCardio(ctx, format):
    decks = PokemonCardIO.GetRandomDeck(format)
    if(decks == None or len(decks) <= 0):
        ctx.send("Could not find any decks!")
    else:
        e = interactions.Embed()
        e.title= f"Random Deck from PokemonCard.io"
        e.color = interactions.BrandColors.YELLOW
        e.set_footer(text="Powered by PokemonCard.io",icon_url="https://images.pokemoncard.io/images/assets/cropped-applogo_high-1-192x192.png")
        deckNames = ""
        for deck in decks:
            deckNames += f"[{deck['deck_name']}]({deck['url']}) created by [{deck['deck_uploader']}]({deck['deck_uploader_profile']}) ({deck['deck_views']} :eye:)\n"

        e.add_field(name="Decks",value=deckNames,inline=False)
    
        await ctx.send(embeds = e)

@interactions.slash_command(name='card_text',
        description="Shows cards that contain this text (must be 3 characters or more)",
        options=[
            interactions.SlashCommandOption(
                name="text",
                description="Text on the card",
                type=interactions.OptionType.STRING,
                required=True
            ),     
            interactions.SlashCommandOption(
                name="set",
                description="Name of the set",
                type=interactions.OptionType.STRING,
                required=False,
                autocomplete=True
            ),  
            interactions.SlashCommandOption(
                name="format",
                description="Check just a specific format",
                type=interactions.OptionType.STRING,
                required=False,                
                choices=[
                    interactions.SlashCommandChoice(
                        name="Standard",
                        value="standard"
                    ),
                    interactions.SlashCommandChoice(
                        name="Expanded",
                        value="expanded"
                    ),
                    interactions.SlashCommandChoice(
                        name="GLC",
                        value="glc"
                    )]
            )]
        )
async def GetSpecificCardText(ctx, text, set = "", format = ""):
    await ctx.defer()
    user = ctx.author
    userId = ctx.author.id
    count = 0
    locale = GetLocaleForUser(userId)
    ALLCARDS = GetAllCardsForLocale(locale)    
    text = HelperFunctions.ReplaceCharacters(text)
    if(set and format == ""):
        suggestions = f"Could not find card containing `\"{text}\" in {set}`\n"
    elif(set and format):
        suggestions = f"Could not find card containing `\"{text}\" in {set} and {format}`\n"
    elif(format):
        suggestions = f"Could not find cards containing `\"{text}\"` in {format}`\n"
    else:        
        suggestions = f"Could not find cards containing `\"{text}\"`\n"
    embeddedArray = []
    foundCard = False
    for val in ALLCARDS.cards:
        if set and format == "":
            if text.lower() in val['cardText'].lower() and len(text) > 3 \
            and val['set']['name'].lower() == set.lower():
                thumbnail = EnergyType.GetEnergyTypeImage(val)  
                e = await BuildEmbed(ctx,val,False,thumbnail)
                embeddedArray.append(e)
                foundCard = True
        elif set and format:
            if text.lower() in val['cardText'].lower() and len(text) > 3 \
            and val['set']['name'].lower() == set.lower() \
            and val['set'][f"{format}Legal"]:
                thumbnail = EnergyType.GetEnergyTypeImage(val)  
                e = await BuildEmbed(ctx,val,False,thumbnail)
                embeddedArray.append(e)
                foundCard = True
        elif format:
            if text.lower() in val['cardText'].lower() and len(text) > 3 \
            and val['set'][f"{format}Legal"]:
                thumbnail = EnergyType.GetEnergyTypeImage(val)  
                e = await BuildEmbed(ctx,val,False,thumbnail)
                embeddedArray.append(e)
                foundCard = True
        else:
            if (text.lower() in val['cardText'].lower() and len(text) > 3): 
                thumbnail = EnergyType.GetEnergyTypeImage(val) 
                e = await BuildEmbed(ctx,val,False,thumbnail)
                embeddedArray.append(e)
                foundCard = True    

    if not foundCard:
        e = interactions.Embed()
        e.title= "Whoa! I can't find that card!"
        e.description = suggestions
        e.color = interactions.BrandColors.RED
        e.set_thumbnail(url = Consts.SAD_FACE)
        embeddedArray.append(e)
    
    maxEmbed = len(embeddedArray)
    
    async def ButtonClick(button_ctx: interactions.ComponentContext):
        try:
            nonlocal count
            if button_ctx.ctx.custom_id == f"prev{ctx.id}" and button_ctx.ctx.author == user:
                if count - 1 >= 0:                        
                    count = count - 1
                    await button_ctx.ctx.edit(embeds = embeddedArray[count])
                else:
                    count = maxEmbed - 1
                    await button_ctx.ctx.edit(embeds = embeddedArray[count])
            elif button_ctx.ctx.custom_id == f"next{ctx.id}" and button_ctx.ctx.author == user:
                if count + 1 < maxEmbed:
                    count = count + 1
                    await button_ctx.ctx.edit(embeds = embeddedArray[count])
                else:
                    count = 0
                    await button_ctx.ctx.edit(embeds = embeddedArray[count])                        
            else:
                try:                                                    
                    await button_ctx.ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
                except:
                    pass
        except:
            pass
        
    if maxEmbed > 1:  
        descCount = 0
        for es in embeddedArray:
            descCount = descCount + 1
            es.description = "Showing " + str(descCount) + "/" + str(maxEmbed) + ". Traverse the cards with the buttons below."


        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="Previous",
                custom_id=f"prev{ctx.id}"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="Next",
                custom_id=f"next{ctx.id}"
            )
        ]
        action_row = interactions.ActionRow(*buttons)
        await ctx.send(embeds = embeddedArray[0], components=[action_row])
        try:       
            button_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=ButtonClick, timeout=60)  
        except asyncio.TimeoutError:
            pass
            # When it times out, edit the original message and remove the button(s)
            # return await ctx.edit(embeds = embeddedArray[count], components=[])  
    else:        
        msg = await ctx.send(embeds = embeddedArray[0]) 

@GetSpecificCardText.autocomplete("set")
async def autocomplete_cardtextset(ctx):
    try:
        choices = [
            interactions.SlashCommandChoice(name=item, value=item) for item in cardBuddy.setDict.autocompleteNames if ctx.kwargs['set'].lower() in item.lower()
        ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.send(choices)
    except:
        pass

@interactions.Task.create(interactions.IntervalTrigger(minutes=10))
async def ListServers():
    if(Consts.TOPGG_AUTHTOKEN is not None):
        async with aiohttp.ClientSession() as session:
            headers = {
                    'Content-Type': "application/json",
                    'Authorization': f"Bearer {Consts.TOPGG_AUTHTOKEN}",
                    'Accept': "*/*",
                    'Host': "top.gg",
                    }
            servercount = len(client.guilds)
            async with session.post(url="https://top.gg/api/bots/642081991071891469/stats", json={'server_count': servercount}, headers=headers) as response:                
                print("List Server POST Status:", response.status)

@interactions.listen()
async def on_startup():
    await client.change_presence(activity="Pokémon TCG")
    ListServers.start()


client.start()

