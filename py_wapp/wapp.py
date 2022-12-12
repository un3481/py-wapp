
##########################################################################################################################

# Imports
from requests import post
from datetime import datetime
from typing import TypedDict

# Modules
from .message import Message
from .reply import Reply

##########################################################################################################################

# Target Type
class ITarget(TypedDict):
    address: str
    user: str
    password: str

##########################################################################################################################

# Whatsapp Class
class Wapp:

    __target__: 'ITarget'
    __referer__: 'ITarget'

    @property
    def wapp(self): return self
    
    ##########################################################################################################################

    # Init Message
    def __init__(
        self,
        target: 'ITarget',
        referer: 'ITarget' = None
    ):
        # Set Default Target
        self.__target__ = None
        self.__referer__ = None

        # Default target Object
        self.set_target(target=target, isref=False)
        self.set_target(target=referer, isref=True)
        
        # Set Reply Object
        self.__reply__ = Reply(self)

    ##########################################################################################################################

    # Set wapp Target
    def set_target(
        self,
        target: 'ITarget',
        isref: bool = False
    ):
        # Default target Object
        tar: 'ITarget' = {
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

    # Request Target
    def req(
        self,
        action: str,
        target: 'ITarget' = None,
        data = None
    ):
        # Set Default Target
        if not isinstance(target, dict):
            target = self.__target__
        
        # Request
        address = target["address"]
        res = post(
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
        json = res.json()
        if not isinstance(json, dict): raise Exception('bad response')
        if 'ok' not in json: raise Exception('bad response')
        
        # Check Status
        if not json['ok']:
            if 'error' not in json:
                raise Exception('target error: (unknown)')
            else:
                raise Exception(f'target error: ({json["error"]})')
        
        # Check Data
        if 'data' not in json: raise Exception('key "data" not found')
        
        # Return Data
        return json['data']
    
    ##########################################################################################################################

    # Request Target Safe
    def reqs(
        self,
        action: str,
        target: 'ITarget' = None,
        data = None
    ):
        try:
            res = self.req(
                action=action,
                target=target,
                data=data
            )
            return True, res
        except Exception as error:
            return False, error

    ##########################################################################################################################

    # Send Message
    def send(
        self,
        to: str,
        text: str = None,
        log: str = None,
        quote: str = None,
        target: 'ITarget' = None,
        referer: 'ITarget' = None
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
        (ok, data) = self.reqs(
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
        if not ok: raise Exception(
            f'failed to send message: ({data})'
        )

        # Construct Message
        sent = Message(
            wapp=self.wapp,
            message=data
        )

        # Log Sent Message
        if not isinstance(log, str): log = 'bot::send'
        print(f'({datetime.now()}) Sent({log}) To({to})')

        # Return Sent
        return sent
    
    ##########################################################################################################################

    # Send Message Safe
    def sends(
        self,
        to: str,
        text: str = None,
        log: str = None,
        quote: str = None,
        target: 'ITarget' = None,
        referer: 'ITarget' = None
    ):
        try:
            data = self.send(
                to=to,
                text=text,
                log=log,
                quote=quote,
                target=target,
                referer=referer
            )
            return True, data
        except Exception as error:
            return False, error

    ##########################################################################################################################

    # Get Host Device
    def get_host_device(self, target: 'ITarget' = None) -> dict:
        # Request Data
        (ok, data) = self.reqs(
            target=target,
            action='getHostDevice'
        )
        
        # Check Response
        if not ok: raise Exception(
            f'failed to get host device: ({data})'
        )
        
        # Return Data
        return data

##########################################################################################################################
