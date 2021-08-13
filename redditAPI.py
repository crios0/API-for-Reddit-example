import json
import urllib
import requests
import requests.auth
#Define variables necessary for making a request via the function api_call
# URI defines the endpoint necessary for accessing endpoints that require
# authentication via OAuth.
# BASE_URI defines the endpoint necessary for generating a session token, with
# the session token generating a bearer ID necessary for inputting into the headers.
URI = "https://oauth.reddit.com"

BASE_URI = "https://www.reddit.com"

AUTHENTICATED_ENDPOINTS = ["/api/v1/me", "/api/v1/me/blocked",
                           "/api/v1/me/prefs", "/api/v1/me/karma",
                           "/api/v1/me/trophies", "/api/v1/me/friends", "/prefs/blocked", "/prefs/friends", "/prefs/messaging", "/prefs/trusted"]

class REDDIT():
    def __init__(self, client_id, client_scrt, username, password):
        self.client_id = client_id
        self.client_scrt = client_scrt
        self.username = username
        self.password = password
        self.access_token = ""

    #api_call takes variables passed to it, and constructs an endpoint, and
    #then based on the parameters and request passed to it, will make an HTTP
    #request to the endpoint.
    def api_call(self, method, params={}, req='GET'):
        headers = {"User-Agent": "crios0 by crios0", "Authorization": "bearer "
        + self.access_token}
        URIAPI = ""
        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_scrt)
        #for endpoints that need a session token in the headers
        if method in AUTHENTICATED_ENDPOINTS:
            URIAPI = URI
        else:
            #This is the URI used for authenticating a token
            URIAPI = BASE_URI
        URIAPI = URIAPI + method
        if req == 'GET':
            params = urllib.parse.urlencode(params)
            URIAPI = URIAPI + params
            response = requests.get(URIAPI, headers=headers)
        elif req == 'POST':
            response = requests.post(URIAPI, data=params, headers=headers)
        elif req == 'PATCH':
            response =  requests.patch(URIAPI, data=params, headers=headers)
        elif req == 'AUTH':
            #When generating a session token, you only need to define the user
            #agent in the header, so it must be as I've defined below.
            headers = {"User-Agent": "crios0 by crios0"}
            post_data = {"grant_type": "password", "username": self.username, "password": self.password}
            response = requests.post("https://www.reddit.com/api/v1/access_token",
            auth=client_auth, data=post_data, headers=headers)
            token = json.loads(response.text)
            self.access_token = token['access_token']
        else:
            pass
        return self._handle_response(response, method)

    #This function will handle the response received from the server. If you
    #receive an error code, then it will return it for the user. If you
    #receive a successful 200 HTTP response then you will receive the JSON
    #response from the server.
    def _handle_response(self, request, method):
        if str(request.status_code).startswith("200"):
            return request.json()
        else:
            return request
#define functions that make use of the api_call function to connect to an
#endpoint specified in the variables you pass to api_call.
    def get_token(self):
        return self.api_call("", "", "AUTH")

    def get_user(self):
        return self.api_call("/api/v1/me", "", "GET")
    
    def get_user_pref(self):
        return self.api_call("/api/v1/me/prefs", "", "GET")

    def patch_user_pref(self, params):
        return self.api_call("/api/v1/me/prefs", params, "PATCH")
    
    def get_user_karma(self):
        return self.api_call("/api/v1/me/karma", "", "GET")

    def get_trophies(self):
        return self.api_call("/api/v1/me/trophies", "", "GET")

    def get_friends(self):
        return self.api_call("/api/v1/me/friends", "", "GET")

    def get_prefs_blocked(self):
        return self.api_call("/prefs/blocked", "", "GET")

    def get_prefs_friends(self):
        return self.api_call("/prefs/friends", "", "GET")

    def get_prefs_messaging(self):
        return self.api_call("/prefs/messaging", "", "GET")

    def get_prefs_trusted(self):
        return self.api_call("/prefs/trusted", "", "GET")
