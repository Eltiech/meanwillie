"""
sex.py - Wraps the "sex" command.
"""
import subprocess

def sex(bot, trigger):
    """.sex - Spouts a mad-lib style erotic statement"""
    bot.say(subprocess.check_output("sex|tr -d '\n'",shell=True))
sex.commands = ['sex']
sex.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()
