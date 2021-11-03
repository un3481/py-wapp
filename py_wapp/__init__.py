
##########################################################################################################################
#                                                       PY-AVBOT                                                         #
##########################################################################################################################
#                                                                                                                        #
#                                                 Whatsapp Bot for AVB                                                   #
#                                          Multi-language API for Whatsapp Bot                                           #
#                             ---------------- Python3 -- NodeJS -- MySQL ----------------                               #
#                                                * Under Development *                                                   #
#                                     https://github.com/anthony-freitas/ts-avbot                                        #
#                                                                                                                        #
##########################################################################################################################
#                                                      MAIN CODE                                                         #
##########################################################################################################################

# Imports
import json
import flask
import py_misc

# Import Local Modules
from .modules import wapp
from .modules import sql
from .modules import chat
from .modules import actions
from .modules import interface

# Make Wapp Available
Wapp = wapp.Wapp

#################################################################################################################################################

Request = flask.request
Response = flask.Response

##########################################################################################################################
#                                                         BOT CLASS                                                      #
##########################################################################################################################

# Bot Class
class Bot:

    # Init Bot
    def __init__(
        self,
        target: dict[str, str | dict[str, str]],
        referer: dict[str, str | dict[str, str]] = None
    ):
        # Set Bot SQL Object
        self.sql = sql.SQL()
        
        # Set Bot Wapp Object
        self.wapp = wapp.Wapp(target, referer)
        
        # Set Bot Chat Object
        self.chat = chat.Chat(self.wapp)
        
        # Set Bot Info
        self.hostd = None
        
        ##########################################################################################################################
        
        # Set Bot Api
        self.api = py_misc.API(log=False).host('0.0.0.0')

        # Set Bot Actions
        self.actions = actions.Actions('/bot/', self.api)
        
        # Set Bot Interface Actions
        self.i = interface.Interface(
            actions.Actions('/i/', self.api)
        )
        
        ##########################################################################################################################
        
        # Add On-Reply Action
        self.i.add('on_reply')(
            self.wapp.__reply__.__execute__
        )
        
        # Add Action Send
        @self.add('send_msg')
        def __send__(req: Request, res: Response) -> Response:
            data = self.bot.send(
                req['to'] if 'to' in req else None,
                req['text'] if 'text' in req else None,
                req['log'] if 'log' in req else None,
                req['quote_id'] if 'quote_id' in req else None
            )
            return res(
                json=json.dumps(data),
                mimetype='application/json',
                status=200
            )
    
    ##########################################################################################################################
    #                                                       BOT METHODS                                                      #
    ##########################################################################################################################

    @property
    def bot(self): return self
    
    # Class Reference
    Wapp = Wapp
    Message = Wapp.Message
    Reply = Wapp.Reply
    
    ##########################################################################################################################
    
    # Keep Alive
    def keepalive(self):
        return py_misc.keepalive()
    
    # Logging
    def log(
        self,
        log: str | Exception,
        console: bool = True,
        mysql: bool = True
    ):
        return py_misc.log(
            log=log,
            console=console,
            mysql=mysql
        )
    
    # MySQL Connection
    def sqlconn(self, mysqlconn: py_misc.MySQL):
        return self.sql.sqlconn(mysqlconn)
        
    ##########################################################################################################################
        
    # Set Port
    def port(self, port: int):
        self.api.port(port)
        return self
    
    # Set User
    def user(self, user: str):
        return self.actions.user(user)

    # Set Pasword
    def password(self, password: str):
        return self.actions.password(password)
    
    ##########################################################################################################################
    
    def target(self):
        return self.wapp.__target__
    
    ##########################################################################################################################

    # Add Action
    def add(self, name: str, log: bool = True):
        return self.actions.add(name, log)

    # Check Request
    def check(
        self,
        req: dict,
        param: str,
        clas: type | None = None
    ):
        return self.actions.check(req, param, clas)

    # Send Message
    def send(
        self,
        to: str,
        text: str,
        log: str = 'api::send_msg',
        quote: str = None,
        target: dict[str, str | dict[str, str]] = None,
        referer: dict[str, str | dict[str, str]] = None
    ) -> Wapp.Message | None:
        return self.wapp.send(
            to=to,
            text=text,
            log=log,
            quote=quote,
            target=target,
            referer=referer
        )
    
    ##########################################################################################################################

    # Start API App
    def start(self):
        # Start MySQL Connection
        self.sql.start()
        # Start Bot Server
        if not self.api.start():
            raise Exception('Flask Server not started')
        # Start Interface Service
        hostd = self.i.start(self.wapp)
        if hostd == None:
            raise Exception('Bot Interface not started')
        # Update Bot Info
        self.hostd = hostd
        self.chat.__replace__.update({
            self.hostd['wid']['user'] : ''
        })
        # Get Bot-Name
        bot_name = self.hostd['name']
        # Log Finished
        py_misc.log(
            log=f'{bot_name}::started'
        )

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
