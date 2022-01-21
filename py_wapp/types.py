
##########################################################################################################################

# Imports
from flask import Request
from typing import TypedDict, Callable, Optional, Any

##########################################################################################################################

def TypeOfBot():
    from .. import Bot
    return Bot

# Bot Type Reference
TBot = (lambda do: TypeOfBot() if do else None)(False)
TWapp = TBot.Wapp if TBot != None else None
TMessage = TWapp.Message if TWapp != None else None
TReply = TWapp.Reply if TWapp != None else None

##########################################################################################################################

# Target Type
class ITarget(TypedDict):
    address: str
    user: str
    password: str

##########################################################################################################################

# Message Reserved Type
IReservedMessage = TypedDict(
    'IReservedMessage',
    { 'from': str }
)

# Message Type
class IMessage(IReservedMessage):
    id: str
    to: str
    body: str
    author: str
    isGroupMsg: str
    quotedMsgObj: Optional['IMessage']

##########################################################################################################################

# Execute Type
TExec = Callable[[IMessage], Any]

# Execute Action Type
TAExec = Callable[[Request], Any]

##########################################################################################################################
