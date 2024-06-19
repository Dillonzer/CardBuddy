class HelperFunctions:
    
    @staticmethod
    def ReplaceCharacters(word):        
        word = word.lower().replace('-gx', ' gx')
        word = word.lower().replace('-ex', ' ex')
        word = word.lower().replace('-union', ' union')
        word = word.replace('`', '\'')
        word = word.replace('’', '\'')        
        word = word.replace('‘', '\'')
        word = word.replace('“', '\"')
        word = word.replace('”', '\"') 
        if("wait and see hammer" not in word.lower()):
            word = word.lower().replace(" and ", " & ")
        
        if("poké" in word.lower()):
            word = word.lower().replace("poké", "poke")

        return word.strip()     

    @staticmethod
    def edits1(word):
            letters    = 'abcdefghijklmnopqrstuvwxyz-é\'&.(): '
            splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
            deletes    = [L + R[1:]               for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
            replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
            inserts    = [L + c + R               for L, R in splits for c in letters]
            return set(deletes + transposes + replaces + inserts)

    @staticmethod
    def edits2(word): 
        return (e2 for e1 in HelperFunctions.edits1(word) for e2 in HelperFunctions.edits1(e1))

    @staticmethod
    def GetEmoji(name):           
        if(name[-4:] == " {*}"):
            name = name.replace(" {*}", " <:prism:885930754985590824>")
        if(" Delta Species" in name):
            name = name.replace(" Delta Species", " δ")
        if(name[-5:] == " Star"):
            name = name.replace(" Star", " <:star:885930754838790144>")       
        if("Darkness Energy" in name):
            name = name.replace("Darkness ","<:darkness:885952208967983155> ")
        if("Water Energy" in name):
            name = name.replace("Water ","<:water:885952208917651456> ")
        if("Psychic Energy" in name):
            name = name.replace("Psychic ","<:psychic:885952209068625980> ")
        if("Metal Energy" in name):
            name = name.replace("Metal ","<:metal:885952208888275044> ")
        if("Lightning Energy" in name):
            name = name.replace("Lightning ","<:lightning:885952208846348359> ")
        if("Grass Energy" in name):
            name = name.replace("Grass ","<:grass:885952208934436904> ")
        if("Fire Energy" in name):
            name = name.replace("Fire ","<:fire:885952208913448980> ")
        if("Fighting Energy" in name):
            name = name.replace("Fighting ","<:fighting:885952209089593344> ")
        if("Fairy Energy" in name):
            name = name.replace("Fairy ","<:fairy:885952208875716628> ")
        if("Dragon Energy" in name):
            name = name.replace("Dragon ","<:dragon:885952209009905664> ")
        if("Colorless Energy" in name):
            name = name.replace("Colorless ","<:colorless:885952208527560725> ")
        if("Energy FDY" in name):
            name = name.replace(" FDY"," <:fighting:885952209089593344><:darkness:885952208967983155><:fairy:885952208875716628>")
        if("Energy GRW" in name):
            name = name.replace(" GRW"," <:grass:885952208934436904><:fire:885952208913448980><:water:885952208917651456>")
        if("Energy LPM" in name):
            name = name.replace(" LPM"," <:lightning:885952208846348359><:psychic:885952209068625980><:metal:885952208888275044>")
        if("Energy GRPD" in name):
            name = name.replace(" GRPD"," <:grass:885952208934436904><:fire:885952208913448980><:psychic:885952209068625980><:darkness:885952208967983155>")
        if("Energy WLFM" in name):
            name = name.replace(" WLFM"," <:water:885952208917651456><:lightning:885952208846348359><:fighting:885952209089593344><:metal:885952208888275044>")

        return name

    @staticmethod
    def GetEmojiForNumber(name):
        if(name[-1:] == "A"):
            name = name.replace("A", "<:alternate:885930754683576321>")
        
        return name