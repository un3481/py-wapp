
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
import flask
import typing
import py_misc

# Import Local Modules
from .modules import wapp
from .modules import network
from .modules import chat
from .modules import sql

# Import Types
from .modules.types import ITarget

# Reference Classes
Wapp = wapp.Wapp
NetworkWapp = network.NetworkWapp
Chat = chat.Chat
SQL = sql.SQL

#################################################################################################################################################

Request = flask.request
Response = flask.Response

##########################################################################################################################
#                                                         BOT CLASS                                                      #
##########################################################################################################################

# Bot Class
class Bot:

    # Types
    wapp: 'Wapp'
    network: 'NetworkWapp'
    chat: 'Chat'
    sql: 'SQL'
    hd: dict

    # Init Bot
    def __init__(
        self,
        target: ITarget,
        referer: ITarget = None
    ):
        # Set Bot Wapp Object
        self.wapp = Wapp(
            target=target,
            referer=referer
        )

        # Set Bot Actions
        self.network = NetworkWapp(self)
        
        # Set Bot Chat Object
        self.chat = Chat(self)

        # Set Bot SQL Object
        self.sql = SQL(self)

        # Set Bot Info
        self.hd = None
    
    ##########################################################################################################################

    @property
    def bot(self): return self
    
    # Class Reference
    Wapp = Wapp
    Message = Wapp.Message
    Reply = Wapp.Reply
    NetworkWapp = NetworkWapp

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
        target: ITarget,
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
        json: dict,
        param: str,
        clas: type | typing.Tuple[type] = None
    ):
        return self.network.check(
            json=json,
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
        target: ITarget = None,
        referer: ITarget = None
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
        target: ITarget = None,
        referer: ITarget = None
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
        self.chat.replace.update({
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
