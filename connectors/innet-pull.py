"""INNET API fetch script to inject latest data into UGZ backend"""

import requests

from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

from db.env import env, check_env


class TokenHelper:
    def __init__(self, url: str, client_name: str, client_secret: str):
        self.url = url
        self.client_name = client_name
        self.client_secret = client_secret

    def get_token(self):
        url = f"{self.url}/realms/innet/protocol/openid-connect/token"
        payload = "grant_type=client_credentials"
        # proxies = {"http_proxy", "proxy...."} # proxies disabled ATM
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            auth=HTTPBasicAuth(self.client_name, self.client_secret),
        ).json()
        return response["access_token"], datetime.now() + timedelta(
            seconds=response["expires_in"]
        )

# data = requests.request(
#     "GET",
#     f"https://data.{env['INNET_HOST']}/v1/timeseries/measurements",
#     params={"logger_id": logger.id},
#     headers=auth_header,
# )


# def fetch_active_site_data(
#     innet_auth_header: dict, active_sites: list[Site]
# ):
#     for site in active_sites:
#         # get the loggers related to each site
#         logger_installations = requests.request(
#             "GET",
#             f"https://meta.{env['INNET_HOST']}/v1/site/{site.id}/logger_installations",
#             params={"site_id": site.id},
#             headers=auth_header,
#         )

#         # then save the loggers in the DB
#         upsert_loggers(session, logger_installations.json())

#     loggers = session.query(Logger).filter_by(active=True).all()

#     print("Fetching active loggers")

    # refresh_innet_sites(session, auth_header)

    # active_sites: list(Site) = (
    #     session.query(Site).filter_by(provider_id="innet", active=True).all()
    # )
    # fetch_active_site_data(session, auth_header, active_sites)


if __name__ == "__main__":
    try:
        check_env()

        # Get authentication token
        helper = TokenHelper(f"https://id.{env['INNET_HOST']}", env['INNET_CLIENT_NAME'], env['INNET_CLIENT_SECRET'])

        # Assume script execution complete before INNET token expiry
        token, expires_at = helper.get_token()

        innet_auth_header = {"Authorization": "Bearer " + token}
        sk_db_auth_header = {"Authorization": "Bearer " + env['CONNECTOR_API_TOKEN']}

        # Fetch internal index of INNET loggers
        loggers = requests.request("GET", f"{env['API_BASE_URL']}/loggers", headers=sk_db_auth_header).json()

        for logger in loggers['data']:
            logger['deveui']

    except Exception as e:
        print(f"An error occurred: {e}")
