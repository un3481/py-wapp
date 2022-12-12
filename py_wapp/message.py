
##########################################################################################################################

# Modules
from .common import TWapp, IMessage, TExec

##########################################################################################################################

# Message Class
class Message:

    wapp: 'TWapp'
    on: 'MessageTrigger'
    raw: 'IMessage'

    @property
    def id(self):
        return self.raw.get('id')
    @property
    def to(self):
        return self.raw.get('to')
    @property
    def body(self):
        return self.raw.get('body')
    @property
    def author(self):
        return (
            self.raw.get('author')
            if self.raw.get('isGroupMsg')
            else self.raw.get('from')
        )
    @property
    def quoted(self):
        return (
            Message(
                wapp=self.wapp,
                message=self.raw.get('quotedMsgObj')
            )
            if self.raw.get('quotedMsgObj')
            else None
        )
    
    ##########################################################################################################################
    
    # Init Message
    def __init__(
        self,
        wapp: 'TWapp',
        message: 'IMessage' = None
    ):
        # Set Referece
        self.wapp = wapp
        
        # Set Raw Message
        if isinstance(message, dict):
            self.raw = message
        else: self.raw = IMessage()

        # Set Message-Trigger
        self.on = MessageTrigger(message=self)

    ##########################################################################################################################

    # Quote Message
    def send(
        self,
        text: str = None,
        log: str = None,
        quote: str = None
    ):
        return self.wapp.send(
            to=self.author,
            text=text,
            log=log if log else f'message({self.id})::send',
            quote=quote
        )

    ##########################################################################################################################

    # Quote Message
    def quote(
        self,
        text: str = None,
        log: str = None
    ):
        return self.send(
            text=text,
            log=log if log else f'message({self.id})::quote',
            quote=self.id
        )

##########################################################################################################################

# Message-Trigger
class MessageTrigger:
    
    __message__: 'Message'
    __on_reply__: 'TExec'
    
    @property
    def wapp(self):
        return self.__message__.wapp

    ##########################################################################################################################

    def __init__(self, message: 'Message'):
        # Set Message
        self.__message__ = message

        # Set Default Reply
        self.__on_reply__ = (lambda m: None)

    ##########################################################################################################################

    # Reply Trigger
    def reply(
        self,
        function: TExec
    ):
        # Check Message
        if not isinstance(self.__message__.id, str):
            return function
        
        def on_reply(m: Message):
            try:
                return True, function(m)
            except Exception as error:
                return False, error
        
        # Assign On-Reply Trigger
        self.__on_reply__ = on_reply
        self.wapp.__reply__.add(
            id=self.__message__.id,
            do=self.__on_reply__
        )
        # Return Decorated Function
        return self.__on_reply__

##########################################################################################################################
