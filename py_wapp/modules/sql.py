
##########################################################################################################################

# Imports
import py_misc

# Modules
from .types import TBot

##########################################################################################################################
#                                                            SQL                                                         #
##########################################################################################################################

# SQL Class
class SQL:

    # Types
    bot: TBot
    __conn__: bool

    # Init SQL
    def __init__(self, bot: TBot):
        # Refrence Bot
        self.bot = bot
        # Set Connection Status Object
        self.__conn__ = None
    
    # Set SQL Connection
    def sqlconn(self, mysqlconn: py_misc.MySQL):
        # Set MySQL Objects
        self.mysql = mysqlconn
        self.user = self.mysql.kwargs['user']
        self.password = self.mysql.kwargs['password']
        # Set Logs SQL Connection
        py_misc.log.sqlconn(self.mysql)

    # Check MySQL Link
    def __link__(self):
        try: # Try Connection
            conn = self.mysql.conn
            if self.__conn__ != conn:
                self.__conn__ = conn
                l1 = 'Connection with MySQL Established'
                l2 = 'No Connection with MySQL'
                log = l1 if conn else l2
                self.bot.log(log=log)
            return self.__conn__
        except: return False
    
    # Start MySQL Connection
    def start(self):
        # Check Link Cyclically
        py_misc.schedule.each.five.seconds.do(
            self.__link__
        )
        # Return Done
        return True
            
##########################################################################################################################
#                                                            SQL                                                         #
##########################################################################################################################
