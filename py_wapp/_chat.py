##########################################################################################################################
#                                                      CHAT CLASS                                                        #
##########################################################################################################################

        # Chat Class
        class Chat:
            @property
            def bot(self): return bot

            # Clean Message
            def clean(self, message, lower=True):
                if isinstance(message, Message):
                    strin = self.bot.misc.copy.deepcopy(message.body)
                elif isinstance(message, str):
                    strin = self.bot.misc.copy.deepcopy(message)
                else: return False
                strin = strin.lower() if lower else strin
                strin = strin.replace(self.bot.id, '')
                while '  ' in strin:
                    strin = strin.replace('  ', ' ')
                strin = strin.strip()
                strin = self.bot.misc.unidecode.unidecode(strin)
                return strin

            # Check for Affirmative
            def yes(self, message=None):
                affirm = ['sim', 'positivo', 'correto', 'certo', 'isso']
                if message == None:
                    return self.bot.misc.random.choice(affirm)
                else:
                    return self.clean(message) in affirm

            # Check for Negative
            def no(self, message=None):
                neg = ['nao', 'negativo', 'errado']
                if message == None:
                    return self.bot.misc.random.choice(neg)
                else: return self.clean(message) in neg

            # Get Timedelta as String
            def timedelta(self, t):
                hd = t.seconds // 3600
                h = (t.days * 24) + hd
                m = (t.seconds - (hd * 3600)) // 60
                delta = '{} hora'.format(h) if h != 0 else ''
                delta += 's' if h > 1 else ''
                delta += ' e ' if h != 0 and m != 0 else ''
                delta += '{} minuto'.format(m) if m != 0 else ''
                delta += 's' if m > 1 else ''
                return delta

            @property
            def error(self):
                class Error:
                    @property
                    def bot(self):
                        return bot

                    @property
                    def understand(self):
                        p = [
                            'Desculpe, não entendi o que você quis dizer.',
                            'Sinceramente não entendi o que você falou.',
                            'Não fui capaz de interpretar o que você disse.',
                        ]
                        return self.bot.misc.random.choice(p)

                return Error()