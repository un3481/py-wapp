
##########################################################################################################################

# Imports
from datetime import datetime

# Modules
from .wapp import Wapp
from .chat import Chat
from .network import Network

# Types
from .types import ITarget

##########################################################################################################################
#                                                         BOT CLASS                                                      #
##########################################################################################################################

# Bot Class
class Bot:

    # Types
    wapp: 'Wapp'
    network: 'Network'
    chat: 'Chat'
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
        self.network = Network(self)
        
        # Set Bot Chat Object
        self.chat = Chat(self)

        # Set Bot Info
        self.hd = None
    
    ##########################################################################################################################

    @property
    def bot(self): return self
    
    ##########################################################################################################################
    #                                                       BOT METHODS                                                      #
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
        clas: type | tuple[type] = None
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
        print(f'({datetime.now()}) {name}::started')

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
