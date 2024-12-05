import requests



def send_request(url, 
                method='POST', 
                data=None,
                file=None,
                headers = None):
    try:
        if file:
            response = requests.post(url, data=data, files=file, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'GET':
            response = requests.get(url, params=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, json=data, headers=headers)
        else:
            return {"message": "Notog‘ri HTTP usuli"}, 400
        return response.json(), response.status_code
    except Exception as e:
        return {"message": str(e)}, 500
    