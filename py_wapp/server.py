
##########################################################################################################################

# Imports
from json import loads, dumps
from flask import Flask, request, Request, Response
from flask_httpauth import HTTPBasicAuth

# Modules
from .common import TWapp, TAExec

##########################################################################################################################

# Class Actions
class Server:

    wapp: 'TWapp'
    auth: HTTPBasicAuth
    users: dict[str, str]
    
    @property
    def server(self): return self
    
    ##########################################################################################################################
    
    # Init Actions
    def __init__(self, wapp: 'TWapp'):
        # Reference Bot
        self.wapp = wapp
        
        # Add Authentication
        self.users = {}
        self.auth = HTTPBasicAuth()
        
        # Basic Auth Verification
        @self.auth.verify_password
        def verify_password(user, pwd):
            if user in self.users and self.users.get(user) == pwd:
                return user

    ##########################################################################################################################
    
    # Execute Action
    def __execute__(
        self,
        action: str,
        do: 'TAExec',
        req: Request
    ):
        try:
            ip = req.remote_addr
            print(f'Exec(network::{action}) From({ip})')
            
            # Execute Action
            data = do(req)
            
            # Serialize
            try:
                try: data = loads(dumps(data))
                except: data = loads(dumps(data.__dict__))
            except: data = None
            
            # Return Data
            return {'ok': True, 'data': data}
        
        # If Error Occurred
        except Exception as error:
            # Log Error
            print(f'Throw(network::{action}) Catch({error})')
            
            # Return Error
            return {'ok': False, 'error': f'{error}'}

    ##########################################################################################################################
    
    # Route GET -> Host Device
    def route_get_host_device(self, route: str, app: Flask):
        # Route
        @app.route(f'{route}/host_device', methods=['GET'])
        @self.auth.login_required
        def host_device():
            data = self.__execute__(
                req=request,
                action='get_host_device',
                do=(lambda r: self.wapp.get_host_device()),
            )
            return Response(
                dumps(data),
                mimetype='application/json',
                status=200
            )
        
    ##########################################################################################################################
    
    # Route POST -> On Reply
    def route_post_on_reply(self, route: str, app: Flask):
        # Route
        @app.route(f'{route}/on_reply', methods=['POST'])
        @self.auth.login_required
        def on_reply():
            data = self.__execute__(
                req=request,
                action='on_reply',
                do=(lambda r: self.wapp.__reply__.__execute__(r)),
            )
            return Response(
                dumps(data),
                mimetype='application/json',
                status=200
            )
            
    ##########################################################################################################################
    
    # Route POST -> Send
    def route_post_send(self, route: str, app: Flask):
        # Send Function
        def _send(req: Request):
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
        
        # Route
        @app.route(f'{route}/send', methods=['POST'])
        @self.auth.login_required
        def send():
            data = self.__execute__(
                req=request,
                action='send',
                do=_send,
            )
            return Response(
                dumps(data),
                mimetype='application/json',
                status=200
            )
    
    ##########################################################################################################################
    
    # Route All endpoints
    def route(self, route: str, app: Flask):
        # Route
        self.route_get_host_device(route, app)
        self.route_post_on_reply(route, app)
        self.route_post_send(route, app)
        
        # Return Done
        return True

##########################################################################################################################
     
    