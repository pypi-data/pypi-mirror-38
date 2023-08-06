
from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_rollbox_underlyings_with_rolls import ResponseRollboxUnderlyingsWithRolls


class RequestRollboxUnderlyingsWithRolls:
    """
    """

    def __init__(self,
                 underlyings=None):
        """
        """
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/frb',
                   'endpoint': '/v1/underlyingswithrolls'}
        self.url = Util.build_url(dic_url)
        self.li_undl = [] if underlyings is None else underlyings
        self.dic_input = {'underlyings': self.li_undl}

    def info(self):
        """
        """
        md = """
A RequestRollboxUnderlyingsWithRolls object has the properties:
+ `url`: {}
+ `dic_input`: user input (dict)

and the methods:
+ `call_api()` to make the request to the url
        """.format(self.url)
        return Markdown(md)

    def call_api(self,
                 api,
                 debug=False):
        """
        See https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Explore/Explore_01
        """
        t0 = timer()
        print('calling API...')
        self.dic_api = self.dic_input
        raw_response = api.get(self.url, payload=self.dic_api)
        t1 = timer()
        print('done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseRollboxUnderlyingsWithRolls(raw_response, self.dic_api)
        return response
