"""
slap.py - Slap Module
Copyright 2009, Michael Yanovich, yanovich.net

http://willie.dftba.net
"""

import random

def slap(willie, trigger):
    """.slap <target> - Slaps <target>"""
    text = trigger.group().split()
    if len(text) < 2 or text[1].startswith('#'): return
    if text[1] == willie.nick:
        if (trigger.nick not in willie.config.admins):
            text[1] = trigger.nick
        else: text[1] = 'itself'
    if text[1] in willie.config.admins:
        if (trigger.nick not in willie.config.admins):
            text[1] = trigger.nick
    attacks = [
      "slaps",
      "kicks",
      "destroys",
      "annihilates",
      "roundhouse kicks",
      "rusty hooks",
      "wingslaps",
      "hoofstomps",
      "Berry Punches",
      "laser beams",
      "bucks",
      "suplexes",
      "insults",
      "Flutterstares",
      "Twieyes",
      "backhoofs",
      "suffocates",
      "guilt trips",
      "flies up to the stratosphere and drops",
      "threatens legal action against",
      "neuters",
      "violently neuters",
      "shoves",
      "yells at",
    ]

    verb = random.choice(attacks)
    willie.write(['PRIVMSG', trigger.sender, ' :\x01ACTION', verb, text[1], '\x01'])
slap.commands = ['slap', 'slaps']
slap.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()
