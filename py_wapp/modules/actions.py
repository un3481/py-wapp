
##########################################################################################################################

# Imports
import json
import inspect
import py_misc
import flask

#################################################################################################################################################

Request = flask.request
Response = flask.Response

##########################################################################################################################

# Class Actions
class Actions:
    
    # Init Actions
    def __init__(self, route: str, api: py_misc.API):
        # Add API Execute Actions
        self.__api__ = api
        self.__route__ = self.__api__.route(
            route,
            methods=['GET', 'POST']
        )(
            self.__execute__
        )
        # Actions Dictionary
        self.__actions__ = dict()
        
    @property
    def actions(self): return self
    
    # Set User
    def user(self, user: str):
        return self.__route__.user(user)
    
    # Set Pasword
    def password(self, password: str):
        return self.__route__.password(password)
    
    # Check Request
    def check(self, req: dict, param: str, clas: type = None):
        cond = isinstance(req, dict) and isinstance(param, str) and param in req
        # Check Class
        if cond and inspect.isclass(clas):
            try:  # Check for Iterable
                iter(clas)
                cond = any(isinstance(req[param], c) for c in clas)
            except: cond = isinstance(req[param], clas)
        # Return Condtion
        return cond
    
    ##########################################################################################################################

    # Add Action
    def add(self, name: str, log: bool = True):
        def __decorator__(function):
            # Check Parameters
            if not callable(function): return
            if not isinstance(name, str): return
            if len(name) == 0: return
            # Set Caller
            function = py_misc.call.Safe(function)
            function.__name__ = name
            function.__logging__ = log
            # Nest Objects
            self.__actions__[name] = function
            # Return Function
            return function
        # Return Decorator
        return __decorator__
    
    ##########################################################################################################################
    
    # Append Actions
    def append(self, *args, **kwargs):
        # Append Iterator
        def __append__(col):
            for act in col:
                self.add(act)(col[act])
        # Args Append
        for arg in args:
            # If is Dictionary
            if isinstance(arg, dict):
                __append__(arg)
            # If is Iterable
            elif isinstance(arg, list) or isinstance(arg, tuple):
                for col in arg:
                    if isinstance(col, dict):
                        __append__(col)
        # Kwargs Append
        __append__(kwargs)
        # Return True
        return True
    
    ##########################################################################################################################
    
    # Execute Action
    def __execute__(self, req: Request, res: Response) -> Response:
        # Get Parameters
        rjson = req.json
        # Set Data Variable
        data = None
        try: # Try Block
            # Check Parameters
            if not isinstance(rjson, dict): raise Exception('bad request')
            if 'action' not in rjson: raise Exception('key "action" not in request')
            if not isinstance(rjson['action'], str): raise Exception('key "action" not valid')
            if len(rjson['action']) == 0: raise Exception('key "action" not valid')
            if rjson['action'] not in self.__actions__: raise Exception('action not found')
            # Get Action Name
            action = rjson['action']
            # Define Log
            locale = self.__actions__[action].__locale__
            ip = self.__api__.flask.request.remote_addr
            log = f'Exec({locale}) From({ip})'
            # Log Action
            if self.__actions__[action].__logging__:
                py_misc.log(log=log)
            # Execute Action
            data = self.__actions__[action](rjson)
        # If Error Occurred
        except Exception as error:
            return res(
                json.dumps({
                    'done': False,
                    'error': str(error)
                }),
                mimetype='application/json',
                status=200
            )
        # Serialize
        serialize = lambda d: json.loads(json.dumps(d))
        try: # Make Serializable
            try: data = serialize(data)
            except: data = serialize(data.__dict__)
        except: data = None
        # If Success
        return res(
            json.dumps({
                'done': True, 
                'data': data
            }),
            mimetype='application/json',
            status=200
        )

##########################################################################################################################
    