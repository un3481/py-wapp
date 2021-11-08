
##########################################################################################################################

# Imports
import flask
import py_misc
import requests
import typing

#################################################################################################################################################

Request = flask.request
Response = flask.Response

##########################################################################################################################

# Wapp Type Reference
wappType = (lambda do: Wapp if do else None)(False)

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Message Class
class Message:

    # Init Message
    def __init__(
        self,
        wapp: wappType,
        message: dict[str, typing.Any] = None
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

        # Nest Objects 
        self.Trigger = MessageTrigger
        
        # Set Message-Trigger
        self.on = MessageTrigger(message=self)

    ##########################################################################################################################
    
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

    ##########################################################################################################################

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
    def reply(
        self,
        function: typing.Callable[[Message], typing.Any]
    ):
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
    def __init__(self, wapp: wappType):
        # Set Replyables
        self.__replyables__: dict[
            str,
            typing.Callable[[Message], typing.Any]
        ] = dict()
        
        # Set Reference
        self.wapp = wapp

    # Add Reply
    def add(
        self,
        id: str,
        function: typing.Callable[[Message], typing.Any]
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
    def __execute__(self, req: Request):
        # Get Parameters
        reqjson = req.json
        # Check Parameters
        if not isinstance(reqjson, dict): raise Exception('bad request')
        if 'id' not in reqjson: raise Exception('key "id" not valid')
        if reqjson['id'] not in self.__replyables__: raise Exception('key "id" not valid')
        if 'reply' not in reqjson: raise Exception('key "reply" not valid')
        # Get Reply
        reply = reqjson['reply']
        id = reqjson['id']
        # Construct Reply
        reply = Message(wapp=self.wapp, message=reply)
        # Execute Function
        return self.__replyables__[id](reply)

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
        self.__target__ = None
        self.__referer__ = None

        # Default target Object
        self.setTarget(target)
        self.setTarget(referer, True)
        
        # Set Reply Object
        self.__reply__ = Reply(self)

    ##########################################################################################################################

    # Nest Class
    Message = Message
    Reply = Reply

    @property
    def wapp(self): return self

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Set wapp Target
    def setTarget(
        self,
        target: dict[str, str],
        isref: bool = False
    ):
        # Default target Object
        tar: dict[str, str] = {
            'address': None,
            'user': None,
            'password': None
        }
        
        # Set Target Function
        def _settar(t, d):
            if isinstance(t, dict):
                if isinstance(t.get('address'), str):
                    d['address'] = '' + t['address']
                if isinstance(t.get('user'), str):
                    d['user'] = '' + t['user']
                if isinstance(t.get('password'), str):
                    d['password'] = '' + t['password']
            return d
        
        # Set New Properties
        def assign(t):
            if isinstance(t, dict): _settar(t, tar)
            return _settar(target, tar)
    
        try: # Selector for Target or Referer
            if not isref: self.__target__ = assign(self.__target__)
            else: self.__referer__ = assign(self.__referer__)
            # Return Done
            return True
        except: return False

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Request Target
    def req(
        self,
        action: str,
        target: dict[str, str] = None,
        data = None
    ) -> typing.Any:
        # Set Default Target
        if not isinstance(target, dict):
            target = self.__target__
        # Request
        address = target["address"]
        res = requests.post(
            json = data,
            url = f'{address}/{action}',
            auth = (
                target['user'],
                target['password']
            )
        )
        # Check Response
        if res == None: raise Exception('request error: (unknown)')
        if res.status_code != 200: raise Exception(f'request error: ({res.text})')
        # Check Response Json
        resjson = res.json()
        if not isinstance(resjson, dict): raise Exception('bad response')
        if 'done' not in resjson: raise Exception('bad response')
        # Check Status
        if not resjson['done']:
            if 'error' not in resjson:
                raise Exception('target error: (unknown)')
            else:
                raise Exception(f'target error: ({resjson["error"]})')
        # Check Data
        if 'data' not in resjson: raise Exception('key "data" not found')
        # Return Data
        return resjson['data']

    # Request Target Safe
    def reqs(
        self,
        action: str,
        target: dict[str, str] = None,
        data = None
    ) -> typing.Tuple[typing.Any, Exception]:
        try: # Try Block
            resp = self.req(
                action=action,
                target=target,
                data=data
            )
            return (resp, None)
        except Exception as error:
            return (None, error)

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Send Message
    def send(
        self,
        to: str,
        text: str = None,
        log: str = None,
        quote: str = None,
        target: dict[str, str] = None,
        referer: dict[str, str] = None
    ) -> Message:
        # Check Parameters
        if not isinstance(to, str): raise Exception('argument "to" not valid')
        if not isinstance(text, str) or text == None: raise Exception('argument "text" not valid')
        if not isinstance(log, str) or log == None: raise Exception('argument "log" not valid')
        if not isinstance(quote, str) or quote == None: raise Exception('argument "quote" not valid')

        # Get Target
        if not isinstance(target, dict): target = self.__target__
        if not isinstance(referer, dict): referer = self.__referer__

        # Send Message
        (data, error) = self.reqs(
            target=target,
            action='send',
            data={
                'to': to,
                'text': text,
                'log': log,
                'quote': quote,
                'referer': referer
            }
        )
        # Check Response
        if error: raise Exception(
            f'failed to send message: ({error})'
        )

        # Construct Message
        sent = Message(
            wapp=self.wapp,
            message=data
        )

        # Log Sent Message
        if not isinstance(log, str): log = 'bot::send'
        py_misc.log(f'Sent(${log}) To(${to})')

        # Return Sent
        return sent

    # Send Message Safe
    def sends(
        self,
        to: str,
        text: str = None,
        log: str = None,
        quote: str = None,
        target: dict[str, str] = None,
        referer: dict[str, str] = None
    ) -> typing.Tuple[Message, Exception]:
        try: # Try Block
            data = self.send(
                to=to,
                text=text,
                log=log,
                quote=quote,
                target=target,
                referer=referer
            )
            return (data, None)
        except Exception as error:
            return (None, error)

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Get Host Device
    def getHostDevice(self, target: dict[str, str] = None) -> dict:
        # Request Data
        (data, error) = self.reqs(
            target=target,
            action='getHostDevice'
        )
        # Check Response
        if error: raise Exception(
            f'failed to get host device: ({error})'
        )
        # Return Data
        return data

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################