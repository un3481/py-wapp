
##########################################################################################################################

# Imports
from flask import Request

# Modules
from .common import TWapp, TExec
from .message import Message

##########################################################################################################################
   
# Reply Class
class Reply:
    
    wapp: 'TWapp'
    __repliables__: dict[str, 'TExec']
    
    ##########################################################################################################################

    # Init Reply
    def __init__(self, wapp: 'TWapp'):
        # Set Reference
        self.wapp = wapp

        # Set Repliables
        self.__repliables__: dict[str, 'TExec'] = {}
    
    ##########################################################################################################################

    # Add Reply
    def add(
        self,
        id: str,
        do: 'TExec'
    ):
        # Check Parameters
        if not callable(function): return False
        
        # Delete Old Replyable
        try: del self.__repliables__[id]
        except: self.__repliables__[id] = None
        
        def repliable(m: Message):
            try:
                return True, do(m)
            except Exception as error:
                return False, error
        
        # Add to Dictionary
        self.__repliables__[id] = repliable
        return True
    
    ##########################################################################################################################

    # On Reply
    def __execute__(self, req: Request):
        # Get Parameters
        reqjson = req.json
        
        # Check Parameters
        if not isinstance(reqjson, dict): raise Exception('bad request')
        if 'id' not in reqjson: raise Exception('key "id" not valid')
        if reqjson['id'] not in self.__repliables__: raise Exception('key "id" not valid')
        if 'reply' not in reqjson: raise Exception('key "reply" not valid')
        
        # Get Reply
        reply = reqjson['reply']
        id = reqjson['id']
        
        # Construct Reply
        reply = Message(wapp=self.wapp, message=reply)
        
        # Execute Function
        return self.__repliables__[id](reply)
    
##########################################################################################################################
