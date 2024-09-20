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


def query_innet_loggers(field_name: str):
    data = requests.request(
        "GET",
        f"https://data.{env['INNET_HOST']}/v1/timeseries/{field_name}/last_records",
        params={
            "logger_id": deveui,
            "record_count": 1,
            "field": "final",
            "validity": "valid",
        },
        headers=innet_auth_header,
    ).json()

    if (
        "values" not in data
        or not isinstance(data["values"], list)
        or not len(data["values"])
    ):
        raise ValueError("Measurements have no values")

    if (
        "timestamps" not in data
        or not isinstance(data["timestamps"], list)
        or not len(data["timestamps"])
    ):
        raise ValueError("Measurements have no timestamps")

    return data["values"][0], data["timestamps"][0]


if __name__ == "__main__":
    try:
        check_env()

        # Get authentication token
        helper = TokenHelper(
            f"https://id.{env['INNET_HOST']}",
            env["INNET_CLIENT_NAME"],
            env["INNET_CLIENT_SECRET"],
        )

        # Assume script execution complete before INNET token expiry
        token, expires_at = helper.get_token()

        innet_auth_header = {"Authorization": "Bearer " + token}
        sk_db_auth_header = {"Authorization": "Bearer " + env["CONNECTOR_API_TOKEN"]}

        now = datetime.now().isoformat()  # current date in ISO8601 format

        # Fetch internal index of INNET loggers currently installed
        # date filter: either indefinitely installed or in now in active period
        # logic: (inst.end is None or (inst.start <= now && inst.end >= now))
        installations = requests.request(
            "GET",
            f"{env['API_BASE_URL']}/installations",
            headers=sk_db_auth_header,
            params={
                "populate[0]": "logger",
                "populate[1]": "logger.model",
                "filters[$or][0][end][$null]": True,
                "filters[$or][1][$and][0][start][$lte]": now,
                "filters[$or][1][$and][1][end][$gte]": now,
            },
        ).json()

        for installation in installations["data"]:
            logger = installation["logger"]

            deveui = logger["deveui"]
            field_mapping = logger["model"]["field_mapping"]

            print(f"Fetching latest data for logger.id {deveui}")

            for fm in field_mapping:
                sensor_type, field_name = fm["type"], fm["field"]

                # Query INNET REST API for selected loggers' sensor types
                try:
                    # get the value

                    value, timestamp = query_innet_loggers(field_name)
                    print(f"{sensor_type} \t {round(value, 2)} \t {timestamp}")

                    res = requests.request(
                        method="POST",
                        url=f"{env['API_BASE_URL']}/measurements",
                        json={
                            "data": {
                                "value": value,
                                "type": sensor_type,
                                "timestamp": timestamp,
                                "installation": installation["id"],
                            }
                        },
                        headers=sk_db_auth_header,
                    )
                    print(res.status_code)
                    if res.status_code != 200 and res.status_code != 201:
                        raise Exception("Unable to insert data into ugz API")

                except Exception:
                    print(f"Couldn't add {field_name}, ignoring")

            print("\n")

    except Exception as e:
        print(f"An error occurred: {e}")
