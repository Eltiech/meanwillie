"""
thanks.py - FlutterBitch anger module
Author: miggyb
About: http://berrytube.tv/
"""

import random

def thanks(willie, input): 
   greeting = random.choice((
     'Shut up',
     'I hate you',
     'Go away',
     'Eat a boat',
     'Leave me alone',
     'Get bent',
     'Screw you',
     'Nopony loves you',
     'Get out',
     'Go swivel',
     'I\'ve had my genitals on live television, I don\'t need your crap',
     'You\'re not my real mom',
     'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
   ))
   comma = random.choice((' ', ', '))
   punctuation = random.choice(('', '!'))
   willie.say(greeting +  comma + input.nick + punctuation)
#  willie.say("!kickban " + input.nick + " How about you go away forever? *tailwhip*")
 
# Commented regex, but phenny wouldn't take it. Using clusterfuck line
#  thanks.rule = r"""
#     .*$nickname                        # Username
#     (?!                                # Not followed by
#     (\:\s+|\,\s+ )                     # a ': ' or ', '
#     (                                  # then
#        (ask|tell|help|reload|doc) |    # a command, or,
#        (                               # optionally, a language then a space
#           ((af|sq|ar|az|eu|bn|be|bg|ca|zh\-CN|zh\-TW|hr|cs|da|nl|en|eo|et|tl|
#            fi|fr|gl|ka|de|gu|ht|iw|hi|hu|is|id|ga|it|ja|kn|ko|la|lv|lt|mk|ms|mt|
#            no|fa|pl|pt|ro|ru|sr|sk|sl|es|sw|sv|ta|te|th|tr|uk|ur|vi|cy|yi)\s)*
#           \".+\"\?                     # then '"', at least one character, '"?' 
#        )
#     )
#  """


thanks.rule = r'.*$nickname(?!(\:\s+|\,\s+)((ask|tell|help|reload|doc)|(((af|sq|ar|az|eu|bn|be|bg|ca|zh\-CN|zh\-TW|hr|cs|da|nl|en|eo|et|tl|fi|fr|gl|ka|de|gu|ht|iw|hi|hu|is|id|ga|it|ja|kn|ko|la|lv|lt|mk|ms|mt|no|fa|pl|pt|ro|ru|sr|sk|sl|es|sw|sv|ta|te|th|tr|uk|ur|vi|cy|yi)\s)*\".+\"\?)))'
thanks.priority = 'high'

if __name__ == '__main__': 
   print __doc__.strip()
