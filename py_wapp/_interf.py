##########################################################################################################################
#                                                         INTERFACE                                                      #
##########################################################################################################################

# Interface Class
class Interface:
    
    # Init Interface
    def __init__(self, actions):
        # Interface Actions Object
        self.actions = actions
        # Set Connection Status Object
        self.__conn__ = None
    
    @property
    def bot(self): return bot
    
    # Interface
    def req(self, req, ignore=False):
        # Check Parameters
        if not (self.__conn__ or ignore): return False
        try: # Try Request
            r = self.bot.misc.requests.post(
                'http://127.0.0.1:1615/bot',
                auth=('bot', self.actions.__route__.__password__),
                json=req,
            )
        # Handle Error
        except: return False
        # Return Response
        return r
    
    @property
    def conn(self):
        try: # Try Block
            r = self.req(None, True)
            if r == False: raise Exception('Request Failed')
            else: r.raise_for_status()
        except self.bot.misc.requests.exceptions.ConnectionError: return False
        except self.bot.misc.requests.exceptions.HTTPError: return False
        except self.bot.misc.requests.exceptions.Timeout: return False
        except: return False
        return True
    
    # Check Node Link
    def __link__(self):
        # Check for Changes
        conn = self.conn
        if self.__conn__ != conn:
            self.__conn__ = conn
            l1 = 'Connection with Node Established'
            l2 = 'No Connection with Node'
            log = l1 if conn else l2
            self.bot.log(log)
        # Return Connection Status
        return self.__conn__
    
    # Add Action
    def add(self, name, log=True):
        return self.actions.add(name, log)
    
    # Start Interface App
    def start(self):
        # Check Link Cyclically
        self.bot.misc.schedule.each.one.second.do(self.__link__)
        try: # Get Bot Phone Number
            req = self.req(dict(action='host_device'), True)
            data = req.json()['data']
            self.bot.id = data['wid']['user']
        except: return False
        return True