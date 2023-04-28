
##########################################################################################################################

# Imports
from json import loads, dumps
from flask import Flask, request, Request, Response
from flask_httpauth import HTTPBasicAuth

# Modules
from .types import TWapp, TAExec

##########################################################################################################################

# Class Actions
class Server:

    wapp: 'TWapp'
    auth: 'HTTPBasicAuth'
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
    
    # Add On-POST Trigger
    def run_on_request(
        self,
        action: str,
        do: 'TAExec',
        req: Request
    ):
        try:
            ip = req.remote_addr
            print(f'Exec(remote::{action}) From({ip})')
            
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
            print(f'Throw(remote::{action}) Catch({error})')
            
            # Return Error
            return {'ok': False, 'error': f'{error}'}

    ##########################################################################################################################
    
    # Route GET -> Host Device
    def route_get_host_device(self, route: str, app: Flask):
        # Route
        @app.route(f'{route}/host_device', methods=['GET'])
        @self.auth.login_required
        def host_device():
            data = self.run_on_request(
                req=request,
                action='get_host_device',
                do=(lambda r: self.wapp.get_host_device())
            )
            return Response(
                dumps(data),
                mimetype='application/json',
                status=200
            )
            
    ##########################################################################################################################
    
    # Route GET -> Message
    def route_get_message(self, route: str, app: Flask):
        # Get Message Function
        def do_get_mesage(req: Request):
            # Get Input
            reqargs = req.args
            # Check Request
            if not isinstance(reqargs, dict):
                raise Exception('bad request')
            # Send Message
            return self.wapp.get_message(
                chat_id=reqargs.get('chat_id'),
                id=reqargs.get('id')
            )
        
        # Route
        @app.route(f'{route}/message', methods=['GET'])
        @self.auth.login_required
        def get_message():
            data = self.run_on_request(
                req=request,
                action='get_message',
                do=do_get_mesage
            )
            return Response(
                dumps(data),
                mimetype='application/json',
                status=200
            )

    ##########################################################################################################################
    
    # Route POST -> Message
    def route_post_message(self, route: str, app: Flask):
        # Send Function
        def do_post_message(req: Request):
            # Get Input
            reqjson = req.json
            # Check Request
            if not isinstance(reqjson, dict):
                raise Exception('bad request')
            # Send Message
            ok, sent = self.wapp.send(
                to=reqjson.get('to'),
                content=reqjson.get('content'),
                log=reqjson.get('log'),
                options=reqjson.get('options')
            )
            # Check Result
            if ok and not isinstance(sent, Exception):
                referer = reqjson.get('referer')
                # Add On-Reply Trigger
                if isinstance(referer, dict):
                    sent.on.reply(
                        lambda m: self.wapp.remote.post(
                            action='reply',
                            data=m,
                            target=referer
                        )
                    )
                return (True, sent)
            else:
                return (False, sent)
        
        # Route
        @app.route(f'{route}/message', methods=['POST'])
        @self.auth.login_required
        def post_message():
            data = self.run_on_request(
                req=request,
                action='post_message',
                do=do_post_message,
            )
            return Response(
                dumps(data),
                mimetype='application/json',
                status=200
            )

    ##########################################################################################################################
    
    # Route POST -> Reply
    def route_post_reply(self, route: str, app: Flask):
        # Route
        @app.route(f'{route}/reply', methods=['POST'])
        @self.auth.login_required
        def post_reply():
            data = self.run_on_request(
                req=request,
                action='post_reply',
                do=(lambda r: self.wapp.reply.run_on_reply(r))
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
        self.route_get_message(route, app)
        self.route_post_message(route, app)
        self.route_post_reply(route, app)
        
        # Return Done
        return True

##########################################################################################################################
     
    