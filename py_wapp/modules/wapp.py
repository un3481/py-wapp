
##########################################################################################################################

import json
import flask
import py_misc
import requests
from typing import Any, Callable

#################################################################################################################################################

Request = flask.request
Response = flask.Response

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
        
        # Set Reference Object
        wapp = self
        
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
                
                # Get Quoted
                try:
                    q = self.raw_data['quotedMsgObj']
                    self.quoted = self.__class__(q)
                except: q = None
                
                # Cycli Reference
                msg = self
    
                # Message-Trigger
                class MessageTrigger:

                    def __init__(self):
                        # Set Message
                        self.__msg__ = msg
                        # Set Default Reply
                        self.__reply__ = (lambda: None)

                    @property
                    def wapp(self): return wapp

                    # Reply Trigger
                    def reply(self, function: Callable[[Message], Any]):
                        if isinstance(self.__msg__.id, str): return function
                        self.__reply__ = py_misc.call.Safe(function)
                        self.wapp.__reply__.add(self.__msg__.id, self.__reply__)
                        return self.__reply__
                
                # Set Message-Trigger
                self.on = MessageTrigger()

            @property
            def wapp(self): return wapp
            
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
                reply = self.wapp.Message(reply)
                # Execute Function
                data = self.__replyables__[id](reply)
                # Return Data
                return res(
                    json=json.dumps(data),
                    mimetype='application/json',
                    status=200
                )
        
        # Nest Class
        self.Reply = Reply
        
        # Set Reply Object
        self.__reply__ = self.Reply()

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
        sent = self.req(
            {
                'action': 'send_msg',
                'to': to,
                'text': text,
                'log': log,
                'quote_id': quote_id,
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
        sent = self.Message(sent['data'])
        # Logging
        log = 'api::send_msg' if type(log) != str else log
        py_misc.log(log=f'Sent(${log}) To(${to})')
        # Return Sent
        return sent

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################