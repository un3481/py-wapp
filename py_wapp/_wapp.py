
import py_misc
from ._message import Message, Reply

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Whatsapp Class
class Wapp:

    # Init Message
    def __init__(self, misc: py_misc, target, referer=None):
        # Assign Miscellanous Object
        self.misc = misc
        # Set Reply Object
        self.__reply__ = Reply(self)
        # Default target Object
        self.__settarget__(target)
        self.__settarget__(referer, True)

    # Set wapp Target
    def __settarget__(self, target, isref=False):
        # Default target Object
        tar = dict(addr = None,
            auth = dict(user = None, password = None)
        )
        # Set Target Function
        def _settar(t, d):
            if isinstance(t, dict):
                if isinstance(t.get('addr'), str):
                    d['addr'] = '' + t['addr']
                if isinstance(t.get('auth'), dict):
                    if isinstance(t['auth'].get('user'), str):
                        d['auth']['user'] = '' + t['auth']['user']
                    if isinstance(t['auth'].get('password'), str):
                        d['auth']['password'] = '' + t['auth']['password']
            return d
        # Set New Properties
        def _assign(t):
            if isinstance(t, dict): _settar(t, tar)
            return _settar(target, tar)
        # Selector for Target or Referer
        if not isref: self.__target__ = _assign(self.__target__)
        else: self.__referer__ = _assign(self.__referer__)
        # return Done
        return True
    
    # Interface
    def req(self, json, tar=None):
        # Set Default Target
        if tar == None: tar = self.__target__
        try: # Try Request
            r = self.misc.requests.post(
                url = tar['addr'],
                auth = (tar['auth']['user'], tar['auth']['password']),
                json = json,
            )
        # Handle Error
        except: return False
        # Return Response
        return r

    # Send Message
    def send(self, to, text, log='api::send_msg', quote_id=None, target=None, referer=None):
        # Check Parameters
        if (not (isinstance(to, str) or to == None)
            or not (isinstance(text, str) or text == None)
            or not (isinstance(log, str) or log == None)
            or not (isinstance(quote_id, str) or quote_id == None)):
            return False
        # Get Target
        tar = target if target != None else self.__target__
        ref = referer if referer != None else self.__referer__ 
        # Interface Send Message
        sent = self.req(dict(
            action = 'send_msg',
            to = to,
            text = text,
            log = log,
            quote_id = quote_id,
            referer = ref
        ))
        # On Interface Error
        if sent == False: return False
        # Convert to Json
        else: sent = sent.json()
        # Fix Errors
        if 'done' not in sent: return False
        if not sent['done']: return False
        # Construct Message
        sent = Message(self, sent['data'])
        # Logging
        log = 'api::send_msg' if type(log) != str else log
        self.misc.log('Sent({}) To({})'.format(log, to))
        # Return Sent
        return sent

    # Caller to Send
    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################