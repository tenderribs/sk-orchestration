from requests import request
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta


class TokenHelper:
    def __init__(self, url: str, client_name: str, client_secret: str, proxies={}):
        self.url = url
        self.client_name = client_name
        self.client_secret = client_secret
        self.proxies = proxies

    def get_token(self):
        url = f"{self.url}/realms/innet/protocol/openid-connect/token"
        payload = "grant_type=client_credentials"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = request(
            "POST",
            url,
            headers=headers,
            proxies=self.proxies,
            data=payload,
            auth=HTTPBasicAuth(self.client_name, self.client_secret),
        ).json()
        return response["access_token"], datetime.now() + timedelta(
            seconds=response["expires_in"]
        )
