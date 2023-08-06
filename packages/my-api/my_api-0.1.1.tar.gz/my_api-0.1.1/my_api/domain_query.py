import json

import requests


class DomainQuary(object):
    """Get a list of newly added domains filters for a certain day.
    But need to pay attention to:
        1 To filter information, you need to notify THREATBOOK(company name) 
        in advance to call this interface.
        2 The data provided by the API is not displayed on the x.threatbook.cn webpage.
        
    Attributes:
        :param apikey:With the Private API, you need the corresponding apikey. 
            It is different from the Public API apikey registered through 
            the Analysis Platform website. As our business customer or 
            partner, we will deliver your corresponding apikey by mail.
        
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.msg = ""
        self.data = {}
        self.response_code = -4

    def get_data(self, query_date):
        """Get a list of newly added domains filters for a certain day.
        
        :param query_date: The date of the string type, for example: 20180401 on April 1, 2018.
        :return: A new list of domain names, each of which is a string type domain.
        """
        url = "https://x.threatbook.cn/api/v1/domain_moniter/query"
        parameters = {"apikey": self.api_key, "date": query_date}
        try:
            response = requests.post(url, parameters)
        except Exception as e:
            print(e)
        else:
            if response.status_code == 200:
                ret_json = json.loads(response.text)
                return ret_json

            else:
                self.msg = response.status_code, "not fount"
                res = {"data": self.data, "msg": self.msg, "response_code": self.response_code}
                return json.dumps(res)

