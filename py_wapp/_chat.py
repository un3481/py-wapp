
from ._wapp import Wapp

##########################################################################################################################
#                                                   ERROR MESSAGE CLASS                                                  #
##########################################################################################################################


# Error Object
class ErrorMessages:
    # Init Chat Errors
    def __init__(self, wapp: Wapp):
        self.wapp = wapp
    
    @property
    def misc(self):
        return self.wapp.misc
    
    @property
    def understand(self):
        p = [
            'Desculpe, não entendi o que você quis dizer.',
            'Sinceramente não entendi o que você falou.',
            'Não fui capaz de interpretar o que você disse.',
        ]
        return self.misc.random.choice(p)

##########################################################################################################################
#                                                      CHAT CLASS                                                        #
##########################################################################################################################

# Chat Class
class Chat:
    
    # Init Chat Class
    def __init__(self, wapp: Wapp):
        # Set Misc Reference
        self.wapp = wapp
        # Nest Object
        self.error = ErrorMessages(self.wapp)
        # Set To-Replace Dictionary
        self.__replace__ = {
            '  ': ' '
        }
    
    @property
    def misc(self):
        return self.wapp.misc
    
    # Clean Message
    def clean(self, message, lower=True):
        # Select Actual Text
        if isinstance(message, self.wapp.Message):
            strin = self.misc.copy.deepcopy(message.body)
        elif isinstance(message, str):
            strin = self.misc.copy.deepcopy(message)
        else: return False
        # Turn to Lower-Case
        strin = strin.lower() if lower else strin
        # Replace All Strings in Clear Dict
        replace = self.__replace__
        for s in replace:
            while s in strin:
                strin = strin.replace(s, replace[s])
        # Remove Trailing Spaces
        strin = strin.strip()
        # Encode UTF-8
        strin = self.misc.unidecode.unidecode(strin)
        return strin
    
    # Check for Affirmative
    def yes(self, message=None):
        affirm = ['sim', 'positivo', 'correto', 'certo', 'isso']
        if message == None:
            return self.misc.random.choice(affirm)
        else:
            return self.clean(message) in affirm
    
    # Check for Negative
    def no(self, message=None):
        neg = ['nao', 'negativo', 'errado']
        if message == None:
            return self.misc.random.choice(neg)
        else: return self.clean(message) in neg
    
    # Get Timedelta as String
    def timedelta(self, t):
        hd = t.seconds // 3600
        h = (t.days * 24) + hd
        m = (t.seconds - (hd * 3600)) // 60
        delta = '{} hora'.format(h) if h != 0 else ''
        delta += 's' if h > 1 else ''
        delta += ' e ' if h != 0 and m != 0 else ''
        delta += '{} minuto'.format(m) if m != 0 else ''
        delta += 's' if m > 1 else ''
        return delta