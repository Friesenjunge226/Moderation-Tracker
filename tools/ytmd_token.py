import requests

url = "http://localhost:9863/"
auth_url = "auth/requestcode"




def get_token():
    api_version_request = requests.get(f"{url}metadata").json().get("apiVersions")

    if "v1" in api_version_request:
        api_version = "v1"
    elif "v2" in api_version_request:
        api_version = "v2"
    else:
        raise Exception("Error getting api version from YTMDesktop. Please make sure you have YTMDesktop opened.")

    full_auth_url = f"{url}api/{api_version}/{auth_url}"
    
    body = {
        "appId": "friesenbot226", 
        "appName": "Friesenbot226",
        "appVersion": "0.17.2"
    }
    
    response = requests.post(full_auth_url, json = body)
    code = response.json().get("code")
    print(f"Please confirm the code {code} in the YTMDesktop pop-up window...")
    
    body = {
        "appId": "friesenbot226",
        "code": code
    }
    
    response = requests.post(f"{url}api/{api_version}/auth/request", json = body)
    print(response.json())
    

get_token()