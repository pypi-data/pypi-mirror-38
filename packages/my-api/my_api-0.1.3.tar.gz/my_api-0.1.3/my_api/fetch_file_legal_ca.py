import json

import requests


class FetchFile(object):
    """Get the digital certificate information of the file.
    
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

    def get_all(self, resource):
        """Get the digital certificate information of the file.
        
        :param resource: Sample hash to be detected, SHA256 format.
        :return: Returns a json object containing the signature organization
            name and certificate chain information.
        """

        url = "https://x.threatbook.cn/api/v1/file/fetch_file_legal_ca"
        parameter = {"apikey": self.api_key, "resource": resource}
        try:
            response = requests.post(url, parameter)
        except Exception as e:
            print(e)
        else:
            if response.status_code == 200:
                ret_json = json.loads(response.text)
                if ret_json["response_code"] == 0:
                    ret_json["msg"] = "no data"
                return ret_json

            else:
                self.msg = response.status_code, "not fount"
                res = {"data": self.data, "msg": self.msg, "response_code": self.response_code}
                return json.dumps(res)

    def get_legallssuer(self, resource):
        """
        Get the name of the organization that ultimately signed the sample, and the presence of
         the field indicates that the organization is highly trusted.
        :param resource: Sample hash to be detected, SHA256 format.
        :return: Returns a string of the organization name.
        """

        data0 = self.get_all(resource)
        if data0["response_code"] == 1:
            data1 = data0.get("LegalIssuer", {})
            res = {"LegalIssuer": data1, "msg": self.msg, "response_code": 0}
            return res
        else:
            return data0

    def get_cas(self, resource):
        """Get certificate chain information.
        :param resource: Sample hash to be detected, SHA256 format.
        :return: Returns a list of the details of the certificate chain.
        """

        data0 = self.get_all(resource)
        if data0["response_code"] == 1:
            data1 = data0.get("cas", {})
            res = {"cas": data1, "msg": self.msg, "response_code": 0}
            return res
        else:
            return data0

