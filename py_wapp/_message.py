
from ._wapp import Wapp

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Message Class
class Message:

    # Init Message
    def __init__(self, wapp: Wapp, obj=None):
        # Assign Whatsapp Object
        self.wapp = wapp
        # Fix msg
        if type(obj) != dict:
            self.raw_data = {
                'id': None,
                'to': None,
                'body': None,
                'from': None,
                'author': None,
                'isGroupMsg': False,
            }
        else: self.raw_data = obj
        try: # Get Quoted
            q = self.raw_data['quotedMsgObj']
            self.quoted = self.__class__(q)
        except: q = None
        # Set Default Reply
        self.__reply__ = (lambda: None)

    @property
    def misc(self): return self.wapp.misc
    @property
    def id(self): return self.raw_data['id']
    @property
    def to(self): return self.raw_data['to']
    @property
    def body(self): return self.raw_data['body']
    @property
    def __from__(self): return self.raw_data['from']

    @property
    def author(self):
        return (
            self.raw_data['author']
            if self.raw_data['isGroupMsg']
            else self.raw_data['from']
        )

    # On Reply
    def reply(self, function):
        if type(self.id) != str: return function
        self.__reply__ = self.misc.call.safe(function)
        self.wapp.reply.add(self.id, self.__reply__)
        return self.__reply__

    # Quote Message
    def quote(self, msg, log='api::quote_msg'):
        return self.wapp.send(self.author, msg, log, self.id)

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Reply Class
class Reply:

    # Init Reply
    def __init__(self, wapp: Wapp):
        # Assign Whatsapp Object
        self.wapp = wapp
        # Set Replyables
        self.__replyables__ = dict()

    @property
    def misc(self):
        return self.wapp.misc

    # Add Reply
    def add(self, msg_id, function):
        # Check Parameters
        if not callable(function):
            return False
        # Delete Old Replyable
        try: del self.__replyables__[msg_id]
        except: self.__replyables__[msg_id] = None
        # Add to Dictionary
        self.__replyables__[msg_id] = self.misc.call.Safe(function)
        return True

    # On Reply
    def __execute__(self, req):
        # Check Parameters
        if (('msg_id' not in req)
            or (req['msg_id'] not in self.__replyables__)
            or ('reply' not in req)):
            return False
        # Get Reply
        reply = req['reply']
        msg_id = req['msg_id']
        # Construct Reply
        reply = Message(reply)
        # Execute Function
        data = self.__replyables__[msg_id](reply)
        # Return Data
        return data
