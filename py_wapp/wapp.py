
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

    target: 'ITarget'
    referer: 'ITarget'
    reply: Reply

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
        self.target = None
        self.referer = None

        # Default target Object
        self.set_target(target=target, isref=False)
        self.set_target(target=referer, isref=True)
        
        # Set Reply Object
        self.reply = Reply(self)

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
        def settar(t, d):
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
            if isinstance(t, dict): settar(t, tar)
            return settar(target, tar)
    
        try: # Selector for Target or Referer
            if not isref: self.target = assign(self.target)
            else: self.referer = assign(self.referer)
            # Return Done
            return True
        except: return False

    ##########################################################################################################################

    # Request Target
    def req(
        self,
        action: str,
        data: any,
        target: 'ITarget' = None
    ):
        try:
            # Set Default Target
            if not isinstance(target, dict):
                target = self.target

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
            return (True, json['data'])

        except Exception as error:
            return (False, error)

    ##########################################################################################################################

    # Send Message
    def send(
        self,
        to: str,
        content: str,
        log: str = None,
        options: dict[str, any] = None,
        target: 'ITarget' = None,
        referer: 'ITarget' = None
    ):
        try:
            # Check Parameters
            if not isinstance(to, str): raise Exception('argument "to" not valid')
            if not isinstance(content, str): raise Exception('argument "text" not valid')
            if not isinstance(log, str) and log != None: raise Exception('argument "log" not valid')
            if not isinstance(options, dict) and options != None: raise Exception('argument "quote" not valid')

            # Get Target
            if not isinstance(target, dict): target = self.target
            if not isinstance(referer, dict): referer = self.referer

            # Send Message
            (ok, data) = self.reqs(
                target=target,
                action='send',
                data={
                    'to': to,
                    'content': content,
                    'log': log,
                    'options': options,
                    'referer': referer
                }
            )

            # Check Response
            if not ok or isinstance(data, Exception):
                raise data

            # Construct Message
            sent = Message(
                wapp=self.wapp,
                message=data
            )

            # Log Sent Message
            if not isinstance(log, str): log = 'bot::send'
            print(f'({datetime.now()}) Sent({log}) To({to})')

            # Return Sent
            return True, sent

        except Exception as error:
            return False, error

    ##########################################################################################################################

    # Get Host Device
    def get_host_device(self, target: 'ITarget' = None):
        if not isinstance(target, dict): target = self.target
        return self.req(
            target=target,
            action='get_host_device',
            data=None
        )
    
    ##########################################################################################################################

    # Get Message
    def get_message(
        self,
        chat_id: str,
        id: str,
        target: 'ITarget' = None
    ):
        if not isinstance(target, dict): target = self.target
        return self.req(
            target=target,
            action='get_message',
            data={
                'chatId': chat_id,
                'id': id
            }
        )

##########################################################################################################################
