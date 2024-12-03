import requests

def send_request(url, method='GET', data=None):
    """
    Send a POST or GET request to the given URL.

    Args:
        url (str): The endpoint URL.
        method (str): The HTTP method ('POST' or 'GET').
        data (dict, optional): Data to be sent with the request (for POST only). Default is None.

    Returns:
        dict: The response from the server as a dictionary, status code.
    """
    try:
        if method.upper() == 'POST':
            response = requests.post(url, json=data)
        elif method.upper() == 'GET':
            response = requests.get(url, params=data)
        else:
            return {"error": "Invalid HTTP method. Use 'POST' or 'GET'."}
        if response.status_code == 200:
            return response.json(), response.status_code
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}, response.status_code
    except Exception as e:
        return {"error": str(e)}, response.status_code
    