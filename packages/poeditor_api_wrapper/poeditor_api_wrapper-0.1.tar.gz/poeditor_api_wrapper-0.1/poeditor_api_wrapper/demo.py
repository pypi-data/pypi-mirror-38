from poeditor_api_wrapper.api_config import ApiConfig
from poeditor_api_wrapper.api_interface import ApiInterface
from json import dumps


api_config = ApiConfig()

api_config.set_api_token("3249bd3f2b86abcbd615609e45b30f68")
api_config.set_http_proxy("http://165.225.104.32:80")


api_interface = ApiInterface()

api_interface.set_api_config(api_config)

# print(dumps(api_interface.list_projects(), indent=2))

# print(dumps(api_interface.get_project_by_id("36272"), indent=2))

# print(dumps(api_interface.create_project("The Wrapper Test", "It will be awesome if it works"), indent=2))

# print(dumps(api_interface.update_project_settings("224869", name="Shibzz Rocks", description=None, reference_language="fr"), indent=2))

print(dumps(api_interface.delete_project("224869"), indent=2))