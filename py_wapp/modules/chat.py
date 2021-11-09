
##########################################################################################################################

# Imports
import random
import datetime
import unidecode

# Modules
from .types import TBot, TMessage

##########################################################################################################################
#                                                   ERROR MESSAGE CLASS                                                  #
##########################################################################################################################

# Error Object
class ErrorMessages:

    # Types
    bot: 'TBot'

    # Init Chat Errors
    def __init__(self, bot: TBot):
        self.bot = bot
    
    @property
    def understand(self):
        p = [
            'Desculpe, não entendi o que você quis dizer.',
            'Sinceramente não entendi o que você falou.',
            'Não fui capaz de interpretar o que você disse.',
        ]
        return random.choice(p)

##########################################################################################################################
#                                                      CHAT CLASS                                                        #
##########################################################################################################################

# Chat Class
class Chat:

    # Types
    bot: 'TBot'
    error: 'ErrorMessages'
    replace: dict[str, str]
    
    # Init Chat Class
    def __init__(self, bot: TBot):
        # Set Misc Reference
        self.bot = bot

        # Nest Object
        self.error = ErrorMessages(self.bot)

        # Set To-Replace Dictionary
        self.replace = {
            '  ': ' '
        }

    ##########################################################################################################################

    # Clean Message
    def clean(
        self,
        message: str | TMessage,
        lower=True
    ) -> str:
        # Select Text
        if isinstance(message, str):
            strin = f'{message}'
        elif isinstance(message, self.bot.Message):
            strin = f'{message.body}'
        else: raise Exception('invalid argument "message"')

        # Turn to Lower-Case
        strin = strin.lower() if lower else strin

        # Replace All Strings in Clear Dict
        for s in self.replace:
            while s in strin:
                strin = strin.replace(
                    s,
                    self.replace[s]
                )
        
        # Remove Trailing Spaces
        strin = strin.strip()

        # Encode UTF-8
        strin = unidecode.unidecode(strin)

        # Return Parsed String
        return strin

    ##########################################################################################################################
    
    # Check for Affirmative
    def yes(
        self,
        message: str | TMessage = None
    ) -> str:
        affirm = ['sim', 'positivo', 'correto', 'certo', 'isso']
        if message == None: return random.choice(affirm)
        else: return self.clean(message) in affirm
    
    ##########################################################################################################################

    # Check for Negative
    def no(
        self,
        message: str | TMessage = None
    ) -> str:
        neg = ['nao', 'negativo', 'errado']
        if message == None: return random.choice(neg)
        else: return self.clean(message) in neg
    
    ##########################################################################################################################

    # Get Timedelta as String
    def timedelta(self, t: datetime.timedelta) -> str:
        hd = t.seconds // 3600
        h = (t.days * 24) + hd
        m = (t.seconds - (hd * 3600)) // 60
        delta = f'{h} hora' if h != 0 else ''
        delta += 's' if h > 1 else ''
        delta += ' e ' if h != 0 and m != 0 else ''
        delta += f'{m} minuto' if m != 0 else ''
        delta += 's' if m > 1 else ''
        return delta
    
##########################################################################################################################
