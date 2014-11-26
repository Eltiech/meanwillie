"""
urbandictionary.py - look up a definition on UrbanDictionary
"""

from willie.module import commands, rate, NOLIMIT
from willie import web
import json

@commands('urbandictionary', 'urban', 'ud')
@rate(10)
def urbandictionary(bot, trigger):
    """Looks a word up on UrbanDictionary"""

    word = trigger.group(2)
    if not word:
        bot.reply("You didn't give me a word...")
        return NOLIMIT

    data = json.loads(web.get('http://api.urbandictionary.com/v0/define?term=%s' % web.quote(word)))
    defs = data.get('list', [])

    if len(defs) > 0:
        bot.reply('%s - %s' % (defs[0]['word'], defs[0]['definition']))
    else:
        bot.reply('Does that look like a word to you?')
