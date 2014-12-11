"""
slap.py - Slap Module
Copyright 2009, Michael Yanovich, yanovich.net

http://willie.dftba.net
"""

import random
import re

def slap(willie, trigger):
    """.slap <target> - Slaps <target>"""
    text = re.split(r' +',trigger.group(),1)
    if len(text) < 2 or text[1].startswith('#'): return
    #split it on characters that aren't valid nick characters
    invalidNickChars = re.compile(r'[^a-zA-Z0-9_\-\\\[\]\{\}^`\|]')
    #we're case insensitive later, but the set instersection isn't
    nicklikePieces = re.split(invalidNickChars,text[1].lower())
    safeNicks = re.split(invalidNickChars,willie.config.admins.lower())
    safeNicks.append(willie.config.owner.lower())
    safeNicks.append((willie.nick+"").lower())
    safeNicks.append("herself")
    safeNicks.append("himself")
    safeNicks.append("itself")
    safeNickPieces = list(set(nicklikePieces).intersection(safeNicks))
    if safeNickPieces:
        if (trigger.nick not in safeNicks):
            backfireRegex = re.compile(r'(\b' + r'\b|\b'.join(map(re.escape,safeNickPieces)) + r'\b)',flags=re.IGNORECASE)
            text[1] = re.sub(backfireRegex,trigger.nick,text[1])
    #todo: reimplement previous version's autoconverting of the bot's own nick to 'itself'
    #maybe we should give the bot a gender config option?
    #Now that this takes phrases though, we'd need to account for possessives. it's/itself,her/herself,etc
    attacks = [
      "slaps",
      "bitchslaps",
      "tail-whips",
      "kicks",
      "destroys",
      "annihilates",
      "roundhouse-kicks",
#      "rusty hooks", #what even is this?
      "wing-slaps",
      "wing-attacks",
      "hoof-stomps",
      "Berry Punches",
#      "laser beams", #doesn't really fit our bot
      "bucks",
      "suplexes",
      "insults",
      "gives The Stare to",
      "Stares down",
#      "Twieyes", #unclear meaning, doesn't fit
      "backhoofs",
      "suffocates",
      "guilt-trips",
      "air-drops",
#      "threatens legal action against", #weird, kinda tame
#      "neuters", #meh, seems tame when we have the one below
      "violently neuters",
      "shoves",
      "yells at",
      "sicks Angel on",
      "makes critter-food out of",
      "sucks the juice from",
      "dick-chops",
      "cockblocks",
      "hip-checks",
      "neck-snaps",
      "murders",
      "stabs",
      "cuts",
      "dumps water on",
    ]

    verb = random.choice(attacks)
    willie.write(['PRIVMSG', trigger.sender, ' :\x01ACTION', verb+" "+text[1], '\x01'])
slap.commands = ['slap', 'slaps','buck']
slap.priority = 'medium'

if __name__ == '__main__':
    print(__doc__.strip())
