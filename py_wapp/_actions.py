
##########################################################################################################################

import py_misc
import flask

##########################################################################################################################

# Class Actions
class Actions:
    
    # Init Actions
    def __init__(self, misc: py_misc, route: str, api: py_misc.API):
        # Set Misc Reference
        self.misc = misc
        # Add API Execute Actions
        self.__api__ = api
        self.__route__ = self.__api__.route(
            route,
            methods=['GET', 'POST']
        )(self.__execute__)
        # Actions Dictionary
        self.__actions__ = dict()
        
    @property
    def actions(self): return self
    
    # Set User
    def user(self, user):
        return self.__route__.user(user)
    
    # Set Pasword
    def password(self, password):
        return self.__route__.password(password)
    
    # Check Request
    def check(self, req, param: str, clas: type = None):
        cond = isinstance(req, dict) and isinstance(param, str) and param in req
        # Check Class
        if cond and self.misc.inspect.isclass(clas):
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
            if (not callable(function)
                or not isinstance(name, str)
                or len(name) == 0):
                return False
            # Set Caller
            function = self.misc.call.Safe(function)
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
    def __execute__(self, req: flask.request, res: flask.Response) -> flask.Response:
        # Init Variables
        rjson = req.json
        data = None
        # Serialize
        json = self.misc.json
        jsonify = self.misc.flask.jsonify
        serialize = lambda d: json.loads(json.dumps(d))
        try: # Try Block
            # Check Parameters
            if not isinstance(rjson, dict): raise Exception('bad request')
            if 'action' not in rjson: raise Exception('action missing in request')
            if not isinstance(rjson['action'], str): raise Exception('action must be a string')
            if len(rjson['action']) == 0: raise Exception('action not valid')
            if rjson['action'] not in self.__actions__: raise Exception('action not found')
            # Get Action Name
            action = rjson['action']
            # Define Log
            locale = self.__actions__[action].__locale__
            ip = self.__api__.flask.request.remote_addr
            log = 'Exec({}) From({})'.format(locale, ip)
            # Log Action
            if self.__actions__[action].__logging__:
                self.misc.log(log)
            # Execute Action
            data = self.__actions__[action](rjson)
        # If Error Occurred
        except Exception as error:
            return res(
                jsonify(dict(done=False, error=str(error))), 
                status=200
            )
        try: # Make Serializable
            try: data = serialize(data)
            except: data = serialize(data.__dict__)
        except: data = None
        # If Success
        return res(
            jsonify(dict(done=True, data=data)), 
            status=200
        )

##########################################################################################################################
    