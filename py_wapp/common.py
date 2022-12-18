
##########################################################################################################################

# Imports
from flask import Request
from typing import Callable, Any

##########################################################################################################################

# Execute Type
TExec = Callable[['IMessage'], Any]

# Execute Action Type
TAExec = Callable[[Request], Any]

##########################################################################################################################

def wapp(cond):
    if cond: raise Exception()
    from .wapp import Wapp
    return Wapp

# Bot Type Reference
try: TWapp = (lambda: wapp(True))()
except: None

##########################################################################################################################

def message(cond):
    if cond: raise Exception()
    from .message import Message
    return Message

# Bot Type Reference
try: TMessage = (lambda: message(True))()
except: None

##########################################################################################################################

def imessage(cond):
    if cond: raise Exception()
    from .message import IMessage
    return IMessage

# Bot Type Reference
try: IMessage = (lambda: imessage(True))()
except: None

##########################################################################################################################

def reply(cond):
    if cond: raise Exception()
    from .reply import Reply
    return Reply

# Bot Type Reference
try: TReply = (lambda: reply(True))()
except: None

##########################################################################################################################
