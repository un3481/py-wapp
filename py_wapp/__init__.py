##########################################################################################################################
#                                                      AVBOT CORE                                                        #
##########################################################################################################################

# Bot Class
class Bot:

    # Init Bot
    def __init__(self, misc):
        self.misc = misc
        # Allow Info
        bot = self.bot
        # Bot Phone Number
        self.id = ''

        ##########################################################################################################################
        #                                                           SQL                                                          #
        ##########################################################################################################################

        # SQL Class
        class SQL:

            # Init SQL
            def __init__(self):
                # Set Connection Status Object
                self.__conn__ = None

            # Set SQL Connection
            def sqlconn(self, mysqlconn):
                # Set MySQL Objects
                self.mysql = mysqlconn
                self.user = self.mysql.kwargs['user']
                self.password = self.mysql.kwargs['password']
                # Set Logs SQL Connection
                self.bot.misc.log.sqlconn(self.mysql)

            @property
            def bot(self):
                return bot

            # Check MySQL Link
            def __link__(self):
                try: # Try Connection
                    conn = self.mysql.conn
                    if self.__conn__ != conn:
                        self.__conn__ = conn
                        l1 = 'Connection with MySQL Established'
                        l2 = 'No Connection with MySQL'
                        log = l1 if conn else l2
                        self.bot.log(log)
                    return self.__conn__
                except: return False

            # Start MySQL Connection
            def start(self):
                # Check Link Cyclically
                self.bot.misc.schedule.each.one.second.do(self.__link__)

        ##########################################################################################################################
        #                                                      NEST OBJECTS                                                      #
        ##########################################################################################################################

        # Set Bot Api
        self.api = self.misc.API(log=False).host('0.0.0.0').port(1516)

        # Set Bot Actions
        self.actions = Actions('/bot/', self.api)
        self.actions.user('bot').password('vet89u43t0jw234erwedf21sd9R78fe2n2084u')

        # Set Bot Interface Actions
        iactions = Actions('/ibot/', self.api)
        iactions.user('bot').password('ert2tyt3tQ3423rubu99ibasid8hya8da76sd')
        self.interf = Interface(iactions)

        # Set Bot SQL Object
        self.sql = SQL()

        # Set Global Objects
        self.whapp = Whapp()
        self.chat = Chat()

        # Add Action Send
        @self.add('send_msg')
        def __send__(req):
            r = dict(to=None, text=None, log=None, id=None)
            if 'to' in req: r['to'] = req['to']
            if 'text' in req: r['text'] = req['text']
            if 'log' in req: r['log'] = req['log']
            if 'quote_id' in req: r['id'] = req['quote_id']
            sent = self.bot.send(r['to'], r['text'], r['log'], r['id'])
            return sent

    ##########################################################################################################################
    #                                                       BOT METHODS                                                      #
    ##########################################################################################################################

    @property
    def bot(self):
        return self

    # Add Action
    def add(self, name, log=True):
        return self.actions.add(name, log)

    # Check Request
    def check(self, req, param, clas=None):
        return self.actions.check(req, param, clas)

    # Logging
    def log(self, log):
        return self.misc.log(log)

    # MySQL Connection
    def sqlconn(self, mysqlconn):
        self.sql.sqlconn(mysqlconn)

    # Start API App
    def start(self):
        # Start MySQL Connection
        self.bot.sql.start()
        self.bot.misc.time.sleep(0.1)
        # Start Bot Server
        s = self.bot.api.start()
        if not s: raise Exception('Server Not Started')
        self.bot.misc.time.sleep(0.1)
        # Start Interface Service
        i = self.bot.interf.start()
        if not i: raise Exception('Interface Not Started')
        self.bot.misc.time.sleep(0.1)
        # Log Finished
        self.bot.log('Avbot::Started')

    # Keep Alive
    def keepalive(self):
        self.misc.keepalive()

    # Send Message
    def send(self, *args, **kwargs):
        return self.whapp.send(*args, **kwargs)


##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
