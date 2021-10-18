
import py_misc

##########################################################################################################################
#                                                            SQL                                                         #
##########################################################################################################################

# SQL Class
class SQL:

    # Init SQL
    def __init__(self, misc: py_misc):
        # Set Misc Reference
        self.misc = misc
        # Set Connection Status Object
        self.__conn__ = None
    
    # Set SQL Connection
    def sqlconn(self, mysqlconn: py_misc.MySQL):
        # Set MySQL Objects
        self.mysql = mysqlconn
        self.user = self.mysql.kwargs['user']
        self.password = self.mysql.kwargs['password']
        # Set Logs SQL Connection
        self.misc.log.sqlconn(self.mysql)

    # Check MySQL Link
    def __link__(self):
        try: # Try Connection
            conn = self.mysql.conn
            if self.__conn__ != conn:
                self.__conn__ = conn
                l1 = 'Connection with MySQL Established'
                l2 = 'No Connection with MySQL'
                log = l1 if conn else l2
                self.misc.log(log)
            return self.__conn__
        except: return False
    
    # Start MySQL Connection
    def start(self):
        # Check Link Cyclically
        self.misc.schedule.each.one.second.do(self.__link__)
            
##########################################################################################################################
#                                                            SQL                                                         #
##########################################################################################################################
