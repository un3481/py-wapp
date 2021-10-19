
import py_misc
from typing import Any, Callable

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Whatsapp Class
class Wapp:

    # Init Message
    def __init__(
        self,
        misc: py_misc,
        target: dict[str, str | dict[str, str]],
        referer: dict[str, str | dict[str, str]] = None
    ):
        # Assign Miscellanous Object
        self.misc = misc
        # Set Default Target
        self.__target__ = dict(addr = None,
            auth = dict(user = None, password = None)
        )
        # Default target Object
        self.__settarget__(target)
        self.__settarget__(referer, True)
        
        # Set Reference Object
        wapp = self
        
        ##########################################################################################################################
        #                                                          ACTIONS                                                       #
        ##########################################################################################################################

        # Message-Trigger
        class MessageTrigger:
            
            def __init__(self):
                # Set Default Reply
                self.__reply__ = (lambda: None)

            @property
            def wapp(self): return wapp
            @property
            def misc(self): return self.wapp.misc

            # Reply Trigger
            def reply(self, function: Callable[[Any], Any]):
                if type(self.id) != str: return function
                self.__reply__ = self.misc.call.Safe(function)
                self.wapp.__reply__.add(self.id, self.__reply__)
                return self.__reply__

        ##########################################################################################################################
        #                                                          ACTIONS                                                       #
        ##########################################################################################################################

        # Message Class
        class Message:

            # Init Message
            def __init__(
                self,
                obj: dict[str, Any] = None
            ):
                # Assign Whatsapp Object
                self.wapp = wapp
                # Fix msg
                if type(obj) != dict:
                    self.raw_data = {
                        'id': None,
                        'to': None,
                        'body': None,
                        'from': None,
                        'author': None,
                        'isGroupMsg': False,
                    }
                else: self.raw_data = obj
                try: # Get Quoted
                    q = self.raw_data['quotedMsgObj']
                    self.quoted = self.__class__(q)
                except: q = None
                # Set Message-Trigger
                self.on = MessageTrigger(self.wapp)

            @property
            def wapp(self): return wapp
            @property
            def misc(self): return self.wapp.misc

            @property
            def id(self) -> str:
                return self.raw_data['id']
            @property
            def to(self) -> str:
                return self.raw_data['to']
            @property
            def body(self) -> str:
                return self.raw_data['body']
            @property
            def origin(self) -> str:
                return self.raw_data['from']
            @property
            def author(self) -> str:
                return (
                    self.raw_data['author']
                    if self.raw_data['isGroupMsg']
                    else self.raw_data['from']
                )

            # Quote Message
            def quote(self, msg: str, log: str = 'api::quote_msg'):
                return self.wapp.send(self.author, msg, log, self.id)
        
        # Nest Class
        self.Message = Message

        ##########################################################################################################################
        #                                                          ACTIONS                                                       #
        ##########################################################################################################################

        # Reply Class
        class Reply:

            # Init Reply
            def __init__(self):
                # Set Replyables
                self.__replyables__: dict[
                    str,
                    Callable[[Message], Any]
                ] = dict()

            @property
            def wapp(self): return wapp
            @property
            def misc(self): return self.wapp.misc

            # Add Reply
            def add(
                self,
                msg_id: str,
                function: Callable[[Any], Any]
            ):
                # Check Parameters
                if not callable(function):
                    return False
                # Delete Old Replyable
                try: del self.__replyables__[msg_id]
                except: self.__replyables__[msg_id] = None
                # Add to Dictionary
                self.__replyables__[msg_id] = self.misc.call.Safe(function)
                return True

            # On Reply
            def __execute__(self, req):
                # Check Parameters
                if (('msg_id' not in req)
                    or (req['msg_id'] not in self.__replyables__)
                    or ('reply' not in req)):
                    return False
                # Get Reply
                reply = req['reply']
                msg_id = req['msg_id']
                # Construct Reply
                reply = Message(reply)
                # Execute Function
                data = self.__replyables__[msg_id](reply)
                # Return Data
                return data
        
        # Nest Class
        self.Reply = Reply
        
        # Set Reply Object
        self.__reply__ = self.Reply()

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Set wapp Target
    def __settarget__(
        self,
        target: dict[str, str | dict[str, str]],
        isref: bool = False
    ):
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
    
        try: # Selector for Target or Referer
            if not isref: self.__target__ = _assign(self.__target__)
            else: self.__referer__ = _assign(self.__referer__)
            # Return Done
            return True
        except: return False
    
    # Interface
    def req(
        self,
        json,
        target: dict[str, str | dict[str, str]] = None
    ) -> py_misc.requests.Response:
        # Set Default Target
        if target == None:
            target = self.__target__
        try: # Try Request
            r = self.misc.requests.post(
                json = json,
                url = target['addr'],
                auth = (
                    target['auth']['user'],
                    target['auth']['password']
                )
            )
        # Handle Error
        except: return None
        # Return Response
        return r

    # Send Message
    def send(
        self,
        to: str,
        text: str,
        log: str = 'api::send_msg',
        quote_id: str = None,
        target: dict[str, str | dict[str, str]] = None,
        referer: dict[str, str | dict[str, str]] = None
    ):
        # Check Parameters
        if (not (isinstance(to, str) or to == None)
            or not (isinstance(text, str) or text == None)
            or not (isinstance(log, str) or log == None)
            or not (isinstance(quote_id, str) or quote_id == None)):
            return None
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
        ), tar)
        # On Interface Error
        if sent == None: return None
        # Convert to Json
        else: sent = sent.json()
        # Fix Errors
        if 'done' not in sent: return None
        if not sent['done']: return None
        # Construct Message
        sent = self.Message(self, sent['data'])
        # Logging
        log = 'api::send_msg' if type(log) != str else log
        self.misc.log('Sent({}) To({})'.format(log, to))
        # Return Sent
        return sent

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################