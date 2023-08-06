from api_config import ApiConfig
from api_request import api_request_get, api_request_post

class ApiInterface:
    def __init__(self):
        """Constructor
        """

        self.api_config = None
    
    def set_api_config(self, api_config):
        """[Setter for api_config]
        
        Arguments:
            api_config {[ApiConfig]} -- [The api configuration]
        
        Raises:
            Exception -- [Invalid API Configuration Provided]
        """

        if not isinstance(api_config, ApiConfig):
            raise Exception("Invalid api configuration provided.\nApi configuration should be an instance of ApiConfig")
        self.api_config = api_config
    
    def get_payload(self, payload={}):
        """[To create a payload with the API token with the provided data]
        
        Keyword Arguments:
            payload {dict} -- [description] (default: {{}})
        
        Raises:
            Exception -- [Type checking for payload]
            Exception -- [ApiConfig should not be None]
        
        Returns:
            [dict] -- [a payload with the valid data is provided]
        """

        if not isinstance(payload, dict):
            raise Exception("Payload should be of type dictionary")
        else:
            if not isinstance(self.api_config, ApiConfig):
                raise Exception("No API configuration found")
            self.payload = {
                "api_token": self.api_config.get_api_token()
            }
            for key in payload.keys():
                self.payload[key] = payload[key]
        return self.payload

    def list_projects(self):
        """[Function to collect the list of projects on POEditor]
        
        Returns:
            [list] -- [List of Projects]
        """

        return api_request_post("./projects/list", self.get_payload(), self.api_config.get_proxies())
        
    def get_project_by_id(self, id):
        """[Function to collect details for a specific project from POEditor]
        
        Arguments:
            id {[string]} -- [id of the project]
        
        Returns:
            [dict] -- [project of the specific id]
        """

        payload = {"id": id}
        return api_request_post("./projects/view", self.get_payload(payload), self.api_config.get_proxies())
    
    def create_project(self, name, description=None):
        """[Function to create a new project on POeditor]
        
        Arguments:
            name {[string]} -- [name of the project]
        
        Keyword Arguments:
            description {[string]} -- [description of the project] (default: {None})
        
        Returns:
            [dict] -- [the new project created]
        """

        payload = {"name": name}
        if description is not None:
            payload["description"] = description
        return api_request_post("./projects/add", self.get_payload(payload), self.api_config.get_proxies())

    def update_project_settings(self, id, name=None, description=None, reference_language=None):
        """[Function to update the project details for a specific project]
        
        Arguments:
            id {[string]} -- [id of the project]
        
        Keyword Arguments:
            name {[string]} -- [name of the project] (default: {None})
            description {[string]} -- [description of the project] (default: {None})
            reference_language {[string]} -- [reference language of the project] (default: {None})
        
        Returns:
            [dict] -- [project with the updated details]
        """

        payload = {"id": id}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if reference_language is not None:
            payload["reference_language"] = reference_language
        return api_request_post("./projects/update", self.get_payload(payload), self.api_config.get_proxies())
    
    def delete_project(self, id):
        """[Funtion allows you to delete a specific project]
        
        Arguments:
            id {[string]} -- [id of the project]
        
        Returns:
            [str] -- [Message of the porject was deleted]
        """

        payload = {"id": id}
        return api_request_post("./projects/delete", self.get_payload(payload), self.api_config.get_proxies())