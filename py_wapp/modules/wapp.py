
##########################################################################################################################

# Imports
import json
import flask
import py_misc
import requests
from typing import Any, Callable

#################################################################################################################################################

Request = flask.request
Response = flask.Response

##########################################################################################################################

# Wapp Type Reference
def typewapp(ignore: bool):
    if ignore: raise Exception('wapp')
    from . import wapp
    return wapp
try: wapp = typewapp(True)
except: pass

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Get Default Target Object
def default_target() -> dict[str, str | dict[str, str]]:
    return dict(addr = None,
        auth = dict(user = None, password = None)
    )

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Message Class
class Message:

    # Init Message
    def __init__(
        self,
        wapp: wapp.Wapp,
        message: dict[str, Any] = None
    ):
        # Set Referece
        self.wapp = wapp
        
        # Fix msg
        if isinstance(message, dict):
            self.raw_data = message
        else: self.raw_data = {
            'id': None,
            'to': None,
            'body': None,
            'from': None,
            'author': None,
            'isGroupMsg': False,
        }
        try: # Get Quoted
            q = self.raw_data['quotedMsgObj']
            self.quoted = Message(wapp=wapp, message=q)
        except: self.quoted = None
        
        # Set Message-Trigger
        self.on = MessageTrigger(message=self)
        
    Trigger = (lambda: MessageTrigger)()
    
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
    def quote(
        self,
        text: str,
        log: str = 'api::quote_msg'
    ):
        return self.wapp.send(
            to=self.author,
            text=text,
            log=log,
            quote=self.id
        )

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Message-Trigger
class MessageTrigger:

    def __init__(self, message: Message):
        # Set Message
        self.__message__ = message
        # Set Default Reply
        self.__reply__ = (lambda: None)

    @property
    def wapp(self):
        return self.__message__.wapp

    # Reply Trigger
    def reply(self, function: Callable[[Message], Any]):
        if isinstance(self.__msg__.id, str): return function
        self.__reply__ = py_misc.call.Safe(function)
        self.wapp.__reply__.add(self.__msg__.id, self.__reply__)
        return self.__reply__

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################
    
# Reply Class
class Reply:

    # Init Reply
    def __init__(self, wapp: wapp.Wapp):
        # Set Replyables
        self.__replyables__: dict[
            str,
            Callable[[Message], Any]
        ] = dict()
        
        # Set Reference
        self.wapp = wapp

    # Add Reply
    def add(
        self,
        id: str,
        function: Callable[[Message], Any]
    ):
        # Check Parameters
        if not callable(function):
            return False
        # Delete Old Replyable
        try: del self.__replyables__[id]
        except: self.__replyables__[id] = None
        # Add to Dictionary
        self.__replyables__[id] = py_misc.call.Safe(function)
        return True

    # On Reply
    def __execute__(self, req: Request, res: Response) -> Response:
        # Get Parameters
        rjson = req.json
        # Check Parameters
        if not isinstance(rjson, dict): raise Exception('bad request')
        if 'id' not in rjson: raise Exception('key "id" not valid')
        if rjson['id'] not in self.__replyables__: raise Exception('key "id" not valid')
        if 'reply' not in rjson: raise Exception('key "reply" not valid')
        # Get Reply
        reply = rjson['reply']
        id = rjson['id']
        # Construct Reply
        reply = Message(wapp=self.wapp, message=reply)
        # Execute Function
        data = self.__replyables__[id](reply)
        # Return Data
        return res(
            json=json.dumps(data),
            mimetype='application/json',
            status=200
        )

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Whatsapp Class
class Wapp:

    # Init Message
    def __init__(
        self,
        target: dict[str, str | dict[str, str]],
        referer: dict[str, str | dict[str, str]] = None
    ):
        # Set Default Target
        self.__target__ = default_target()
        self.__referer__ = default_target()
        # Default target Object
        self.set_target(target)
        self.set_target(referer, True)
        
        # Set Reply Object
        self.__reply__ = Reply(self)

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################
     
    # Nest Class
    Message = Message
    Reply = Reply

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Set wapp Target
    def set_target(
        self,
        target: dict[str, str | dict[str, str]],
        isref: bool = False
    ):
        # Default target Object
        tar = default_target()
        
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
    ) -> requests.Response:
        # Set Default Target
        if target == None:
            target = self.__target__
        try: # Try Request
            r = requests.post(
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
        text: str = None,
        log: str = None,
        quote: str = None,
        target: dict[str, str | dict[str, str]] = None,
        referer: dict[str, str | dict[str, str]] = None
    ):
        # Check Parameters
        if not (isinstance(to, str)): return
        if not (isinstance(text, str) or text == None): return
        if not (isinstance(log, str) or log == None): return
        if not (isinstance(quote, str) or quote == None): return
        # Get Target
        tar = target if target != None else self.__target__
        ref = referer if referer != None else self.__referer__ 
        # Interface Send Message
        sent = self.req(
            {
                'action': 'send_msg',
                'to': to,
                'text': text,
                'log': log,
                'quote': quote,
                'referer': ref
            },
            tar
        )
        # On Interface Error
        if sent == None: return None
        # Check Status Code
        if sent.status_code != 200: return None
        # Convert to Json
        sent = json.loads(sent.text)
        # Fix Errors
        if 'done' not in sent: return None
        if not sent['done']: return None
        # Construct Message
        sent = Message(wapp=self.wapp, message=sent['data'])
        # Logging
        log = 'api::send_msg' if not isinstance(log, str) else log
        py_misc.log(log=f'Sent(${log}) To(${to})')
        # Return Sent
        return sent

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################