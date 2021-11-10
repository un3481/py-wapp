
##########################################################################################################################

# Imports
import typing
import flask

##########################################################################################################################
#                                                            SQL                                                         #
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
#                                                            SQL                                                         #
##########################################################################################################################

# Target Type
class ITarget(typing.TypedDict):
    address: str
    user: str
    password: str

##########################################################################################################################

# Message Reserved Type
IReservedMessage = typing.TypedDict(
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
    quotedMsgObj: typing.Optional['IMessage']

##########################################################################################################################

# Execute Type
TExec = typing.Callable[[IMessage], typing.Any]

# Execute Action Type
TAExec = typing.Callable[[flask.Request], typing.Any]

##########################################################################################################################
#                                                            SQL                                                         #
##########################################################################################################################
