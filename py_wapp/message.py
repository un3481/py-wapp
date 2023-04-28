
##########################################################################################################################

# Import
from typing import TypedDict

# Modules
from .types import TWapp, TExec

##########################################################################################################################

# Message Reserved Type
IReservedMessage = TypedDict(
    'IReservedMessage',
    { 'from': str }
)

# Message Type
class IMessage(IReservedMessage):
    id: dict[str, str]
    to: str
    body: str
    author: str
    hasQuotedMsg: bool

##########################################################################################################################

# Message Class
class Message:

    wapp: 'TWapp'
    on: 'MessageTrigger'
    raw: 'IMessage'

    @property
    def id(self):
        return self.raw.get('id').get('_serialized')
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
            if self.raw.get('author')
            else self.raw.get('from')
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

    # Get Quoted Message
    def get_quoted_message(self):
        if self.raw.get('hasQuotedMsg'):
            return self.wapp.get_message(
                chat_id=self.raw.get('chatId'),
                id=self.id
            )
        else: return None

    ##########################################################################################################################

    # Reply Message
    def reply(
        self,
        content: str = None,
        log: str = None,
        options: dict[str, any] = None
    ):
        return self.wapp.send(
            to=self.author,
            content=content,
            log=log if log else f'message({self.id})::send',
            options=dict.update(
                { 'quotedMessageId': self.id },
                options
            )
        )

##########################################################################################################################

# Message-Trigger
class MessageTrigger:
    
    message: 'Message'
    on_reply: 'TExec'
    
    @property
    def wapp(self):
        return self.message.wapp

    ##########################################################################################################################

    def __init__(self, message: 'Message'):
        # Set Message
        self.message = message

        # Set Default Reply
        self.on_reply = (lambda m: None)

    ##########################################################################################################################

    # Reply Trigger
    def reply(
        self,
        fun: TExec
    ):
        # Check Message
        if not isinstance(self.message.id, str):
            return fun
        
        # Define Safe Wrapper
        def wrapper(m: Message):
            try:
                return True, fun(m)
            except Exception as error:
                return False, error
        
        # Store Function
        self.on_reply = wrapper
        
        # Assign On-Reply Trigger
        self.wapp.reply.on_reply(
            id=self.message.id,
            do=self.on_reply
        )
        
        # Return Decorated Function
        return self.on_reply

##########################################################################################################################
