class ApiConfig:
    def __init__(self):
        """Constructor
        """
        self.api_token = None
        self.http_proxy = None
        self.https_proxy = None
        
    
    def set_api_token(self, api_token):
        """Setter for api_token
        
        Arguments:
            api_token {String} -- [API token for POEdtior]
        """
        self.api_token = api_token

    def get_api_token(self):
        """ Getter for API Token

        Raises:
            Exception -- [
                No API token found.
                Please provide an API token from POEditor
            ]
        
        Returns:
            [String] -- [POEditor API token]
        """

        if self.api_token is None:
            raise Exception("No API token found.\nPlease provide an API token from POEditor")
        else:
            return self.api_token

    def set_http_proxy(self, http_proxy):
        """setter for http_proxy
        
        Arguments:
            http_proxy {String} -- [http proxy value in http://{host}:{port}]
        """

        self.http_proxy = http_proxy
    
    def set_https_proxy(self, https_proxy):
        """setter for https_proxy
        
        Arguments:
            https_proxy {String} -- [https proxy value in https://{host}:{port}]
        """

        self.https_proxy = https_proxy

    def get_proxies(self):
        """ getter for proxies
        
        Returns:
            [dict] -- [A dictionary of http and https proxy values]
        """

        return {
            "http": self.http_proxy,
            "https": self.https_proxy if self.https_proxy is not None else self.http_proxy
        } if self.http_proxy is not None and self.https_proxy is not None else {}