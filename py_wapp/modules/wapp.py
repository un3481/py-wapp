
##########################################################################################################################

# Imports
import flask
import py_misc
import requests
import typing

# Modules
from .types import ITarget, IMessage, TExec

#################################################################################################################################################

Request = flask.request
Response = flask.Response

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Message Class
class Message:

    # Types
    wapp: 'Wapp'
    Trigger: typing.Type['MessageTrigger']
    on: 'MessageTrigger'
    raw: 'IMessage'

    # Init Message
    def __init__(
        self,
        wapp: 'Wapp',
        message: IMessage = None
    ):
        # Set Referece
        self.wapp = wapp

        # Set Trigger
        self.Trigger = MessageTrigger
        
        # Set Raw Message
        if isinstance(message, dict):
            self.raw = message
        else: self.raw = IMessage()

        # Set Message-Trigger
        self.on = self.Trigger(message=self)

    ##########################################################################################################################
    
    @property
    def id(self):
        return self.raw.get('id')
    @property
    def to(self):
        return self.raw.get('to')
    @property
    def body(self):
        return self.raw.get('body')
    @property
    def author(self):
        return (
            self.raw.get('author')
            if self.raw.get('isGroupMsg')
            else self.raw.get('from')
        )
    @property
    def quoted(self):
        return (
            Message(
                wapp=self.wapp,
                message=self.raw.get('quotedMsgObj')
            )
            if self.raw.get('quotedMsgObj')
            else None
        )
    
    ##########################################################################################################################

    # Quote Message
    def send(
        self,
        text: str = None,
        log: str = None,
        quote: str = None
    ):
        return self.wapp.send(
            to=self.author,
            text=text,
            log=log if log else f'message({self.id})::send',
            quote=quote
        )


    ##########################################################################################################################

    # Quote Message
    def quote(
        self,
        text: str = None,
        log: str = None
    ):
        return self.send(
            text=text,
            log=log if log else f'message({self.id})::quote',
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
        self.__onReply__ = (lambda m: None)

    # Reply Function
    __onReply__: TExec

    @property
    def wapp(self):
        return self.__message__.wapp

    # Reply Trigger
    def reply(
        self,
        function: TExec
    ):
        # Check Message
        if not isinstance(self.__message__.id, str):
            return function
        # Assign On-Reply Trigger
        self.__onReply__ = py_misc.call.Safe(function)
        self.wapp.__reply__.add(
            id=self.__message__.id,
            do=self.__onReply__
        )
        # Return Decorated Function
        return self.__onReply__

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################
    
# Reply Class
class Reply:

    # Init Reply
    def __init__(self, wapp: 'Wapp'):
        # Set Reference
        self.wapp = wapp

        # Set Replyables
        self.__replyables__: dict[str, TExec] = {}

    # Add Reply
    def add(
        self,
        id: str,
        do: TExec
    ):
        # Check Parameters
        if not callable(function):
            return False
        # Delete Old Replyable
        try: del self.__replyables__[id]
        except: self.__replyables__[id] = None
        # Add to Dictionary
        self.__replyables__[id] = py_misc.call.Safe(do)
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
        target: ITarget,
        referer: ITarget = None
    ):
        # Set Default Target
        self.__target__ = None
        self.__referer__ = None

        # Default target Object
        self.setTarget(target=target, isref=False)
        self.setTarget(target=referer, isref=True)
        
        # Set Reply Object
        self.__reply__ = Reply(self)

    ##########################################################################################################################

    # Nest Class
    Message = Message
    Reply = Reply

    # Target
    __target__: ITarget
    __referer__: ITarget

    @property
    def wapp(self): return self

    ##########################################################################################################################
    #                                                          ACTIONS                                                       #
    ##########################################################################################################################

    # Set wapp Target
    def setTarget(
        self,
        target: ITarget,
        isref: bool = False
    ):
        # Default target Object
        tar: ITarget = {
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
        target: ITarget = None,
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
        try: # Check Response Status
            res.raise_for_status()
        except Exception as error:
            raise Exception(f'request error: ({error})')
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
        target: ITarget = None,
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
        target: ITarget = None,
        referer: ITarget = None
    ) -> Message:
        # Check Parameters
        if not isinstance(to, str): raise Exception('argument "to" not valid')
        if not isinstance(text, str) and text != None: raise Exception('argument "text" not valid')
        if not isinstance(log, str) and log != None: raise Exception('argument "log" not valid')
        if not isinstance(quote, str) and quote != None: raise Exception('argument "quote" not valid')

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
        target: ITarget = None,
        referer: ITarget = None
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
    def getHostDevice(self, target: ITarget = None) -> dict:
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