
import py_misc

# Class Actions
class Actions:
    
    # Init Actions
    def __init__(self, misc: py_misc, route: str, api: py_misc.API):
        # Set Misc Reference
        self.misc = misc
        # Add API Execute Actions
        self.__api__ = api
        self.__route__ = self.__api__.add(route, methods=['GET', 'POST'])(self.__execute__)
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
    
    # Execute Action
    def __execute__(self, req):
        data = None
        try: # Try Block
            # Check Parameters
            if not isinstance(req, dict): raise Exception('bad request')
            if 'action' not in req: raise Exception('action missing in request')
            if not isinstance(req['action'], str): raise Exception('action must be a string')
            if len(req['action']) == 0: raise Exception('action not valid')
            if req['action'] not in self.__actions__: raise Exception('action not found')
            # Get Action Name
            action = req['action']
            # Define Log
            locale = self.__actions__[action].__locale__
            ip = self.__api__.flask.request.remote_addr
            log = 'Exec({}) From({})'.format(locale, ip)
            # Log Action
            if self.__actions__[action].__logging__:
                self.misc.log(log)
            # Execute Action
            data = self.__actions__[action](req)
        # If Error Occurred
        except Exception as error:
            return dict(done=False, error=str(error))
        try: # Make Serializable
            json = self.misc.json
            serialize = lambda d: json.loads(json.dumps(d))
            try: data = serialize(data)
            except: data = serialize(data.__dict__)
        except: data = None
        # If Success
        return dict(done=True, data=data)