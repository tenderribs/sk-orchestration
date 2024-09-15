import requests
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth


class TokenHelper:
    def __init__(self, url: str, client_name: str, client_secret: str):
        self.url = url
        self.client_name = client_name
        self.client_secret = client_secret

    def get_token(self):
        url = f"{self.url}/realms/innet/protocol/openid-connect/token"
        payload = "grant_type=client_credentials"
        proxies = {"http_proxy", "proxy...."}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.request(
            "POST",
            url,
            proxies=proxies,
            headers=headers,
            data=payload,
            auth=HTTPBasicAuth(self.client_name, self.client_secret),
        ).json()
        return response["access_token"], datetime.now() + timedelta(seconds=response["expires_in"])
