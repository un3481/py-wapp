
##########################################################################################################################

# Imports
from requests import get, post, Response

# Modules
from .types import TWapp, ITarget

##########################################################################################################################

# Remote Class
class Remote:

    wapp: 'TWapp'
    
    ##########################################################################################################################

    # Init Remote
    def __init__(self, wapp: 'TWapp'):
        # Set Reference
        self.wapp = wapp

    ##########################################################################################################################

    # Handle Response
    def handle_response(
        self,
        res: Response
    ):
        # Check Response
        if res == None: raise Exception('request error: (unknown)')

        try: # Check Response Status
            res.raise_for_status()
        except Exception as error:
            raise Exception(f'request error: ({error})')

        # Check Response Json
        resjson = res.json()
        if not isinstance(resjson, dict): raise Exception('bad response')
        if 'ok' not in resjson: raise Exception('bad response')

        # Check Status
        if not resjson['ok']:
            if 'error' not in resjson:
                raise Exception('target error: (unknown)')
            else:
                raise Exception(f'target error: ({resjson["error"]})')

        # Check Data
        if 'data' not in resjson: raise Exception('key "data" not found')

        # Return Data
        return resjson['data']
    
    ##########################################################################################################################

    # Request Target
    def get(
        self,
        action: str,
        data: dict[str, str],
        target: 'ITarget' = None
    ):
        try:
            # Set Default Target
            if not isinstance(target, dict):
                target = self.wapp.target

            # Request
            address = target["address"]
            res = get(
                url = f'{address}/{action}',
                auth = (
                    target['user'],
                    target['password']
                ),
                params = data
            )

            # Check Response
            data = self.handle_response(res)

            # Return Data
            return (True, data)
        except Exception as error:
            return (False, error)
    
    ##########################################################################################################################

    # Request Target
    def post(
        self,
        action: str,
        data: any,
        target: 'ITarget' = None
    ):
        try:
            # Set Default Target
            if not isinstance(target, dict):
                target = self.wapp.target

            # Request
            address = target["address"]
            res = post(
                url = f'{address}/{action}',
                auth = (
                    target['user'],
                    target['password']
                ),
                json = data
            )

            # Check Response
            data = self.handle_response(res)

            # Return Data
            return (True, data)
        except Exception as error:
            return (False, error)
        
##########################################################################################################################
