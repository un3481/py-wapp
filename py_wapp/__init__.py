
##########################################################################################################################
#                                                       PY-AVBOT                                                         #
##########################################################################################################################
#                                                                                                                        #
#                                                 Whatsapp Bot for AVB                                                   #
#                                          Multi-language API for Whatsapp Bot                                           #
#                             ---------------- Python3 -- NodeJS -- MySQL ----------------                               #
#                                                * Under Development *                                                   #
#                                     https://github.com/anthony-freitas/ts-avbot                                        #
#                                                                                                                        #
##########################################################################################################################
#                                                      MAIN CODE                                                         #
##########################################################################################################################

# Import Miscellaneous
import py_misc as misc

# Import Local Modules
from ._wapp import Wapp
from ._chat import Chat
from ._actions import Actions
from ._interf import Interface

##########################################################################################################################
#                                                         BOT CLASS                                                      #
##########################################################################################################################

# Bot Class
class Bot:

    # Init Bot
    def __init__(self, target):
        
        # Set Misc Reference
        self.misc = misc
        
        ##########################################################################################################################

        # Set Bot SQL Object
        self.sql = SQL(self.misc)
        
        # Set Bot Chat Object
        self.chat = Chat(self.misc)
        
        # Set Bot Wapp Object
        self.wapp = Wapp(self.misc)
        
        ##########################################################################################################################
        
        # Set Bot Info
        self.wapp.__settarget__(target)
        self.hd = None
        
        ##########################################################################################################################
        
        # Set Bot Api
        self.api = self.misc.API(log=False).host('0.0.0.0')

        # Set Bot Actions
        self.actions = Actions(self.misc, '/bot/', self.api)
        
        # Set Bot Interface Actions
        self.i = Interface(
            Actions(self.misc, '/i/', self.api)
        )
        
        ##########################################################################################################################
        
        # Add On-Reply Action
        self.i.add('on_reply')(
            self.wapp.__reply__.__execute__
        )
        
        # Add Action Send
        @self.add('send_msg')
        def __send__(req):
            return self.bot.send(
                req['to'] if 'to' in req else None,
                req['text'] if 'text' in req else None,
                req['log'] if 'log' in req else None,
                req['quote_id'] if 'quote_id' in req else None
            )
    
    ##########################################################################################################################
    #                                                       BOT METHODS                                                      #
    ##########################################################################################################################

    @property
    def bot(self): return self
    
    ##########################################################################################################################
    
    # Keep Alive
    def keepalive(self):
        self.misc.keepalive()
    
    # Logging
    def log(self, log):
        return self.misc.log(log)
    
    # MySQL Connection
    def sqlconn(self, mysqlconn):
        self.sql.sqlconn(mysqlconn)
        
    ##########################################################################################################################
        
    # Set Port
    def port(self, port):
        self.api.port(port)
        return self
    
    # Set User
    def user(self, user):
        return self.actions.user(user)

    # Set Pasword
    def password(self, password):
        return self.actions.password(password)
    
    ##########################################################################################################################
    
    def target(self):
        return self.wapp.__target__
    
    ##########################################################################################################################

    # Add Action
    def add(self, name, log=True):
        return self.actions.add(name, log)

    # Check Request
    def check(self, req, param, clas=None):
        return self.actions.check(req, param, clas)

    # Send Message
    def send(self, *args, **kwargs):
        return self.wapp.send(*args, **kwargs)
    
    ##########################################################################################################################

    # Start API App
    def start(self):
        # Start MySQL Connection
        self.sql.start()
        # Start Bot Server
        if not self.api.start():
            raise Exception('Flask server not started')
        # Start Interface Service
        hd = self.i.start(self.wapp)
        if hd == None:
            raise Exception('Bot Interface not started')
        # Update Bot Info
        self.hd = hd
        self.chat.__replace__.update({
            self.hd['wid']['user'] : ''
        })
        # Log Finished
        self.misc.log(
            self.hd['name'] + '::started'
        )

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
