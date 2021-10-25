
##########################################################################################################################

# Imports
import py_misc
import requests

# Modules
from . import actions
from . import wapp

##########################################################################################################################
#                                                         INTERFACE                                                      #
##########################################################################################################################

# Interface Class
class Interface:
    
    # Init Interface
    def __init__(self, act: actions.Actions):
        # Interface Actions Object
        self.__actions__ = act
        # Set Connection Status Object
        self.__conn__ = None
        
    # Set User
    def user(self, user):
        return self.__actions__.user(user)

    # Set Pasword
    def password(self, password):
        return self.__actions__.password(password)

    @property
    def conn(self):
        try: # Try Block
            r = self.wapp.req(None)
            if r == False: raise Exception('HTTP request to Target failed')
            else: r.raise_for_status()
        except requests.exceptions.ConnectionError: return False
        except requests.exceptions.HTTPError: return False
        except requests.exceptions.Timeout: return False
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
            py_misc.log(log)
        # Return Connection Status
        return self.__conn__
    
    # Add Action
    def add(self, name, log=True):
        return self.__actions__.add(name, log)
    
    # Start Interface App
    def start(self, wa: wapp.Wapp):
        # Assign Wapp
        self.wapp = wa
        # Set Default Value
        data = None
        # Check Link Cyclically
        py_misc.schedule.each.one.second.do(self.__link__)
        try: # Get Bot Phone Number
            req = self.wapp.req({ 'action':'host_device' })
            data = req.json()['data']
        except: return None
        return data
    
##########################################################################################################################
#                                                         INTERFACE                                                      #
##########################################################################################################################
