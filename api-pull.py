import os
import requests
import pandas as pd
from dotenv import load_dotenv
from TokenHelper import TokenHelper

load_dotenv() # Load environment variables from .env file
env = {
    "API_CLIENT_NAME": os.getenv("API_CLIENT_NAME"),
    "API_CLIENT_SECRET": os.getenv("API_CLIENT_SECRET"),
    "API_HOST": os.getenv("API_HOST")
}

# def get_weather_data() -> pd.DataFrame:

#     PARAMS = {
#     }

#     print(proxies)

#     response = requests.get(url=API_ENDPOINT, params=PARAMS, proxies=proxies)
#     response.raise_for_status()  # Raise an exception for bad responses


#     data = response.json()  # Parse JSON response

#     # # Extract relevant data and create DataFrame
#     # df = pd.DataFrame({

#     # })

#     # return df

def check_env() -> None:
    for key, value in env.items():
        if not value: raise ValueError(f"Ensure {key} is set in '.env' file")


def main() -> None:
    check_env()

    helper = TokenHelper(f"https://id.{env["API_HOST"]}", env["API_CLIENT_NAME"], env["API_CLIENT_SECRET"])

    # Get token and expiry date of token
    token, expires_at = helper.get_token()

    auth_header = {"Authorization": "Bearer " + token}
    response = requests.request("GET", f"https://meta.{env["API_HOST"]}/v1/site", headers=auth_header)

    print("META:")
    print(response.json())

    response = requests.request(
        "GET",
        f"https://data.{env["API_HOST"]}/v1/timeseries/measurements",
        params={
            'site_id': 'BueroMEL'
        },
        headers=auth_header,
    )

    print("\nDATA:")
    print(response.json())

    # # Optionally, save to CSV
    # weather_df.to_csv('weather_data.csv', index=False)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
