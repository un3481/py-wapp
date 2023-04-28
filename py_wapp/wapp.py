
##########################################################################################################################

# Imports
from requests import get, post, Response
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

class Remote:
        
    wapp: 'Wapp'
    
    ##########################################################################################################################

    # Init Request
    def __init__(self, wapp: 'Wapp'):
        # Set Reference
        self.wapp = wapp

    ##########################################################################################################################

    # Handle Response
    def handle_response(
        self,
        res: Response
    ):
        # Check Response
        if res == None: raise Exception('request error: (unknown)')

        try: # Check Response Status
            res.raise_for_status()
        except Exception as error:
            raise Exception(f'request error: ({error})')

        # Check Response Json
        resjson = res.json()
        if not isinstance(resjson, dict): raise Exception('bad response')
        if 'ok' not in resjson: raise Exception('bad response')

        # Check Status
        if not resjson['ok']:
            if 'error' not in resjson:
                raise Exception('target error: (unknown)')
            else:
                raise Exception(f'target error: ({resjson["error"]})')

        # Check Data
        if 'data' not in resjson: raise Exception('key "data" not found')

        # Return Data
        return resjson['data']
    
    ##########################################################################################################################

    # Request Target
    def get(
        self,
        action: str,
        data: dict[str, str],
        target: 'ITarget' = None
    ):
        try:
            # Set Default Target
            if not isinstance(target, dict):
                target = self.wapp.target

            # Request
            address = target["address"]
            res = get(
                url = f'{address}/{action}',
                auth = (
                    target['user'],
                    target['password']
                ),
                params = data
            )

            # Check Response
            data = self.handle_response(res)

            # Return Data
            return (True, data)
        except Exception as error:
            return (False, error)
    
    ##########################################################################################################################

    # Request Target
    def post(
        self,
        action: str,
        data: any,
        target: 'ITarget' = None
    ):
        try:
            # Set Default Target
            if not isinstance(target, dict):
                target = self.wapp.target

            # Request
            address = target["address"]
            res = post(
                url = f'{address}/{action}',
                auth = (
                    target['user'],
                    target['password']
                ),
                json = data
            )

            # Check Response
            data = self.handle_response(res)

            # Return Data
            return (True, data)
        except Exception as error:
            return (False, error)
    
##########################################################################################################################

# Whatsapp Class
class Wapp:

    target: 'ITarget'
    referer: 'ITarget'
    remote: 'Remote'
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
        
        # Set Remote Object
        self.remote = Remote(self)
        
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

    # Get Host Device
    def get_host_device(self, target: 'ITarget' = None):
        if not isinstance(target, dict): target = self.target
        return self.remote.get(
            target=target,
            action='host_device',
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
        return self.remote.get(
            target=target,
            action='message',
            data={
                'chat_id': chat_id,
                'id': id
            }
        )

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
            (ok, data) = self.remote.post(
                target=target,
                action='message',
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
            return (True, sent)
        except Exception as error:
            return (False, error)

##########################################################################################################################
