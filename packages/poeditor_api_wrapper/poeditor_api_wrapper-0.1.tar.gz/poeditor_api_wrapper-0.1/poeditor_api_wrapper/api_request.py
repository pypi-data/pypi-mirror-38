from requests import post, get
from urllib import parse as url_parse

def get_api_url(path):
    """[generate the Api url using the main url and the new path]
    
    Arguments:
        path {[string]} -- [end point path]
    
    Raises:
        Exception -- [Invalid path was provided]
    
    Returns:
        [string] -- [API url to ping]
    """

    if path is None:
        raise Exception("No path provided")
    return url_parse.urljoin("https://api.poeditor.com/v2/", path)


def api_request_post(url, data, proxies, files=None):
    """[For HTTP POST call for POEditor with exception error handling]
    
    Arguments:
        url {[string]} -- [The url you want to call]
        data {[dict]} -- [payload for the API call]
        proxies {[dict]} -- [proxies for API call]
        files {[string]} -- [file to upload] 
    
    Raises:
        Exception -- [API Error responses]
    
    Returns:
        [any] -- [Response of the API]
    """

    url = get_api_url(url)
    if files is not None:
        data = post(
            url,
            data=data,
            proxies=proxies
        ).json()
    else:
        data = post(
            url,
            data=data,
            files=files,
            proxies=proxies
        )
    if data["response"]["code"] != "200":
        raise Exception("POEditor API Error: " + data["response"]["message"])
    else:
        return data["result"] if "result" in data.keys() else data["response"]["message"]

def api_request_get(url, proxies):
    """[For HTTP GET call for POEditor]
    
    Arguments:
        url {[string]} -- [The url you want to call]
        proxies {[dict]} -- [proxies for API call]
    
    Returns:
        [any] -- [Response of the API]
    """

    url = get_api_url(url)
    data = get(
        url,
        proxies=proxies
    ).content
    return data
    
