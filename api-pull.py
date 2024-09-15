import os
import requests
import pandas as pd
from dotenv import load_dotenv
from TokenHelper import TokenHelper


# Load environment variables from .env file
load_dotenv()

SECRET = os.getenv("SECRET")

# Get keys from environment variables
http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")

# def get_weather_data() -> pd.DataFrame:

#     PARAMS = {
#     }

#     # # Proxy details
#     # proxies = {
#     #     "http": http_proxy,
#     #     "https": https_proxy
#     # }

#     print(proxies)

#     response = requests.get(url=API_ENDPOINT, params=PARAMS, proxies=proxies)
#     response.raise_for_status()  # Raise an exception for bad responses


#     data = response.json()  # Parse JSON response

#     # # Extract relevant data and create DataFrame
#     # df = pd.DataFrame({

#     # })

#     # return df

if __name__ == "__main__":
    try:
        if not SECRET:
            raise ValueError("Make sure all keys are set in your .env file.")

        helper = TokenHelper("https://id.dev.innet.io", "ugz_test_client_ro", SECRET)

        # Get token and expiry date of token
        token, expires_at = helper.get_token()

        auth_header = {"Authorization": "Bearer " + token}
        response = requests.request("GET", "https://meta.dev.innet.io/v1/site", headers=auth_header)

        print("META:")
        print(response.json())

        response = requests.request(
            "GET",
            "https://data.dev.innet.io/v1/timeseries/measurements?site_id=BueroMEL",
            headers=auth_header,
        )

        print("\nDATA:")
        print(response.json())

        # Optionally, save to CSV
        # weather_df.to_csv('weather_data.csv', index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
