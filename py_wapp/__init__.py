
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
from .modules import network

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
        target: dict[str, str],
        referer: dict[str, str] = None
    ):
        # Set Bot SQL Object
        self.sql = sql.SQL()
        
        # Set Bot Wapp Object
        self.wapp = wapp.Wapp(target, referer)
        
        # Set Bot Chat Object
        self.chat = chat.Chat(self)

        # Set Bot Actions
        self.network = network.NetworkWapp(self)

        # Set Bot Info
        self.hostd = None
    
    ##########################################################################################################################

    @property
    def bot(self): return self
    
    # Class Reference
    Wapp = Wapp
    Message = Wapp.Message
    Reply = Wapp.Reply

    ##########################################################################################################################
    #                                                       BOT METHODS                                                      #
    ##########################################################################################################################
    
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

    # Keep Alive
    def keepalive(self):
        return py_misc.keepalive()
        
    ##########################################################################################################################

    # Set Target
    def setTarget(
        self, 
        target: dict[str, str],
        isref: bool = False
    ):
        return self.wapp.setTarget(
            target=target,
            isref=isref
        )

    # Add Action
    def add(self, action: str):
        return self.network.add(action)

    ##########################################################################################################################

    # Check Request
    def check(
        self,
        req: dict,
        param: str,
        clas: type | None = None
    ):
        return self.actions.check(
            req=req,
            param=param,
            clas=clas
        )

    ##########################################################################################################################

    # Send Message
    def send(
        self,
        to: str,
        text: str = None,
        log: str = None,
        quote: str = None,
        target: dict[str, str] = None,
        referer: dict[str, str] = None
    ) -> Wapp.Message | None:
        return self.wapp.send(
            to=to,
            text=text,
            log=log,
            quote=quote,
            target=target,
            referer=referer
        )
    
    # Send Message
    def sends(
        self,
        to: str,
        text: str = None,
        log: str = None,
        quote: str = None,
        target: dict[str, str] = None,
        referer: dict[str, str] = None
    ) -> Wapp.Message | None:
        return self.wapp.sends(
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
        # Assign Bot Endnode
        self.network.assign()
        # Get Host Device
        hd = self.wapp.getHostDevice()
        # Update Bot Info
        self.hd = hd
        self.chat.__replace__.update({
            (self.hd['wid']['user']) : ''
        })
        # Get Bot Name
        name = self.hd['name']
        # Log Bot Started
        py_misc.log(
            log=f'{name}::started'
        )

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
