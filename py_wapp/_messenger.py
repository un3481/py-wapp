
##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Message Class
class Message:

    # Init Message
    def __init__(self, whapp, obj=None):
        # Assign Whatsapp Object
        self.whapp = whapp
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
    def misc(self): return self.whapp.misc
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
        self.msg.reply.add(self.id, self.__reply__)
        return self.__reply__

    # Quote Message
    def quote(self, msg, log='api::quote_msg'):
        return self.msg.send(self.author, msg, log, self.id)

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Reply Class
class Reply:

    # Init Reply
    def __init__(self, whapp):
        # Assign Whatsapp Object
        self.whapp = whapp
        # Set Replyables
        self.__replyables__ = dict()
        # Add Action
        self.interf.add('on_reply')(self.__execute__)

    @property
    def misc(self): return self.whapp.misc

    # Add Reply
    def add(self, msg_id, function):
        # Check Parameters
        if not callable(function):
            return False
        # Delete Old Replyable
        try: del self.__replyables__[msg_id]
        except: self.__replyables__[msg_id] = None
        # Add to Dictionary
        self.__replyables__[msg_id] = self.misc.call.safe(function)
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
        reply = self.whapp.sent(reply)
        # Execute Function
        data = self.__replyables__[msg_id](reply)
        # Return Data
        return data

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################

# Whatsapp Class
class Whapp:

    # Init Message
    def __init__(self, misc, target, referer):
        # Set Reply
        self.__reply__ = Reply(self)
        # Constructor of Sent Messages
        self.__sent__ = self.bot.misc.construct(Sent)
        # Assign Miscellanous Object
        self.misc = misc
        # Default target Object
        self.__settarget__(target)
        self.__settarget__(referer, True)

    # Set Whapp Target
    def __settarget__(self, target, isref=False):
        # Default target Object
        tar = dict(addr = None,
            auth = dict(user = None, password = None)
        )
        # Set Target Function
        def _settar(t, d):
            if isinstance(t, dict):
                if isinstance(t.get('addr'), str):
                    d['addr'] = '' + t['addr']
                if isinstance(t.get('auth'), dict):
                    if isinstance(t['auth'].get('user'), str):
                        d['auth']['user'] = '' + t['auth']['user']
                    if isinstance(t['auth'].get('password'), str):
                        d['auth']['password'] = '' + t['auth']['password']
            return d
        # Set New Properties
        def _assign(t):
            if isinstance(t, dict): _settar(t, tar)
            return _settar(target, tar)
        # Selector for Target or Referer
        if not isref: self.__target__ = _assign(self.__target__)
        else: self.__referer__ = _assign(self.__referer__)
        # return Done
        return True


    # Send Message
    def send(self, to, text, log='api::send_msg', quote_id=None, target=None, referer=None):
        # Check Parameters
        if (not (isinstance(to, str) or to == None)
            or not (isinstance(text, str) or text == None)
            or not (isinstance(log, str) or log == None)
            or not (isinstance(quote_id, str) or quote_id == None)):
            return False
        # Get Target
        tar = target if target != None else self.__target__
        ref = referer if referer != None else self.__referer__ 
        # Interface Send Message
        sent = self.misc.requests.post(
            url = tar['addr'],
            auth = (tar['auth']['user'], tar['auth']['password'])
            json = dict(
                action='send_msg',
                to = to,
                text = text,
                log = log,
                quote_id = quote_id,
                referer = ref
            )
        )
        # On Interface Error
        if sent == False: return False
        # Convert to Json
        else: sent = sent.json()
        # Fix Errors
        if 'done' not in sent: return False
        if not sent['done']: return False
        # Construct Message
        sent = self.__sent__(self, sent['data'])
        # Logging
        log = 'api::send_msg' if type(log) != str else log
        self.bot.log('Sent({}) To({})'.format(log, to))
        # Return Sent
        return sent

    # Caller to Send
    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)

##########################################################################################################################
#                                                          ACTIONS                                                       #
##########################################################################################################################