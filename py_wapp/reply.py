
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
    repliables: dict[str, 'TExec']
    
    ##########################################################################################################################

    # Init Reply
    def __init__(self, wapp: 'TWapp'):
        # Set Reference
        self.wapp = wapp

        # Set Repliables
        self.repliables: dict[str, 'TExec'] = {}
    
    ##########################################################################################################################

    # Add On-Reply Trigger
    def on_reply(
        self,
        id: str,
        do: 'TExec'
    ):
        # Check Parameters
        if not callable(function): return False
        
        # Delete Old Repliable
        try: del self.repliables[id]
        except: self.repliables[id] = None
        
        def repliable(m: Message):
            try:
                return True, do(m)
            except Exception as error:
                return False, error
        
        # Add to Dictionary
        self.repliables[id] = repliable
        return True
    
    ##########################################################################################################################

    # Run On-Reply Trigger
    def run_on_reply(self, req: Request):
        # Get Parameters
        reqjson = req.json
        
        # Check Parameters
        if not isinstance(reqjson, dict): raise Exception('bad request')
        if 'id' not in reqjson: raise Exception('key "id" not valid')
        if reqjson['id'] not in self.repliables: raise Exception('key "id" not valid')
        if 'reply' not in reqjson: raise Exception('key "reply" not valid')
        
        # Get Reply
        reply = reqjson['reply']
        id = reqjson['id']
        
        # Construct Reply
        reply = Message(wapp=self.wapp, message=reply)
        
        # Execute Function
        return self.repliables[id](reply)
    
##########################################################################################################################
