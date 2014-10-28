"""
poni.py - random poni episode selector for bt

This code is bad and I feel bad. But it works alright I guess.
"""

import os
import sqlite3
import random
import pprint
import re
from willie.module import commands, example, NOLIMIT
import willie.tools

def filename(self):
    return os.path.join(self.config.dotdir, "pont.db")
def smartsay(bot,ep):
    series = ""
    if len(ep)==4:
        series = ep[3] + " - "
    if ep[0] and ep[1]:
        bot.say("%s%dx%s - %s" % (series,ep[0],ep[1],ep[2]))
    elif ep[1]:
        bot.say("%s%s - %s" % (series,ep[1],ep[2]))
    else:
        bot.say("%s - %s" % (series,ep[2]))

def poni(bot,trigger):
    pp = pprint.PrettyPrinter(indent=4)
    print(filename(bot))
    db = sqlite3.connect(filename(bot)).cursor()
    query = trigger.group(2)
    if not query:
        c = db.execute("SELECT season,episode,title FROM pont WHERE canon = 1 AND category = 'episode'").fetchall()
        smartsay(bot, random.choice(c))
    else:
        m = re.match(r"^s(\d)$",query)
        if m:
            c = db.execute("SELECT season,episode,title FROM pont WHERE canon = 1 AND season = %s" % m.group(1)).fetchall()
            smartsay(bot, random.choice(c))
            return
        m = re.match(r"^(rdp|mas|fiw|other)$",query)
        if m:
            c = db.execute('SELECT season,episode,title FROM pont WHERE series = "%s"' % m.group(1)).fetchall()
            smartsay(bot, random.choice(c))
            return
        if query == "all":
            c = db.execute('SELECT season,episode,title,series FROM pont').fetchall()
            smartsay(bot, random.choice(c))
            return
        if query == "noncanon":
            c = db.execute('SELECT season,episode,title,series FROM pont WHERE canon = 0').fetchall()
            smartsay(bot, random.choice(c))
            return
        if query == "help":
            bot.say("usage: .poni (s1|s2|s3|s4|rdp|mas|fiw|other|all|noncanon|movie|episode)")
            return
        m = re.match(r"^(movie|episode)$",query)
        if m:
            c = db.execute('SELECT season,episode,title,series FROM pont WHERE category = %s' % m.group(0)).fetchall()
            smartsay(bot, random.choice(c))
            return




poni.commands = ['poni', 'pont']
poni.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()

    
