
##########################################################################################################################

# Imports
import json
import flask
import inspect
import py_misc
import typing

# Modules
from .types import TBot, TAExec

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

##########################################################################################################################

# Class Actions
class NetworkWapp:

    #Types
    bot: 'TBot'
    users: dict[str, str]
    
    # Init Actions
    def __init__(self, bot: TBot):
        # Reference Bot
        self.bot = bot

        # Add API Execute Actions
        self.users = dict()
    
    @property
    def network(self): return self

    ##########################################################################################################################

    # Check Request
    def check(
        self,
        json: dict,
        param: str,
        clas: type | typing.Tuple[type] = None
    ):
        cond = isinstance(json, dict) and isinstance(param, str) and param in json
        # Check Class
        if cond and inspect.isclass(clas):
            try:  # Check for Iterable
                iter(clas)
                cond = any(isinstance(json[param], c) for c in clas)
            except: cond = isinstance(json[param], clas)
        # Return Condtion
        return cond
    
    ##########################################################################################################################

    # Set Route
    def route(self, route: str, app: py_misc.Express):
        self.__route__ = route
        self.app = app
    
    ##########################################################################################################################

    # Add Action
    def add(self, action: str):
        # Check Parameters
        if not isinstance(action, str): raise Exception('argument "action" not valid')
        if len(action) == 0: raise Exception('argument "action" not valid')
        
        # Decorator
        def __decorator__(
            do: TAExec
        ):
            # Check Parameters
            if not callable(do):
                raise Exception('argument "do" not valid')

            # Set Caller
            dosafe = py_misc.call.Safe(do)
            dosafe.__name__ = action
            dosafe.__logging__ = True

            # Set Route
            decorator = self.app.route(
                route=f'{self.__route__}/{action}',
                methods=['GET', 'POST']
            )

            # Apply Route
            @decorator
            def endnode(req: Request, res: Response) -> Response:
                # Execute
                data = self.__execute__(
                    action=action,
                    do=dosafe,
                    req=req
                )
                # Return Reponse
                return res(
                    json.dumps(data),
                    mimetype='application/json',
                    status=200
                )
            
            # Set Authentication
            endnode.users.update(self.users)

            # Return Function
            return endnode
        
        # Return Decorator
        return __decorator__
    
    ##########################################################################################################################
    
    # Execute Action
    def __execute__(
        self,
        action: str,
        do: TAExec,
        req: Request
    ):
        try: # Try Block
            ip = self.__api__.flask.request.remote_addr
            py_misc.log(f'Exec(network::{action}) From({ip})')
            # Execute Action
            data = do(req)
            # Serialize
            serialize = lambda d: json.loads(json.dumps(d))
            try: # Make Serializable
                try: data = serialize(data)
                except: data = serialize(data.__dict__)
            except: data = None
            # Return Data
            return {
                'done': True, 
                'data': data
            }
        # If Error Occurred
        except Exception as error:
            # Log Error
            py_misc.log(f'Throw(network::{action}) Catch({error})')
            # Return Error
            return {
                'done': False,
                'error': str(error)
            }

    ##########################################################################################################################
    
    # Assign Network Actions
    def assign(self):

        self.network.add('getHostDevice')(
            lambda r: self.bot.wapp.getHostDevice()
        )

        # Add On-Reply Action
        self.network.add('onReply')(
            self.bot.wapp.__reply__.__execute__
        )
        
        # Add Send Action
        @self.network.add('send')
        def __send__(req: Request):
            # Get Input
            reqjson = req.json
            # Check Request
            if not isinstance(reqjson, dict):
                raise Exception('bad request')
            # Send Message
            return self.bot.send(
                to=reqjson.get('to'),
                text=reqjson.get('text'),
                log=reqjson.get('log'),
                quote=reqjson.get('quote')
            )

##########################################################################################################################
     
    