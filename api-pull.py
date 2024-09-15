"""API fetch script to add entries"""

import requests

from sk_env import env, check_env, db_url

from TokenHelper import TokenHelper

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# innet https://portal.dev.innet.io
# meteoblue https://measurements-api.meteoblue.com/v2/docs

# def innet_fetch() -> pd.DataFrame:
#     project_id: str = "bac738bc-5e8e-48ca-8e73-84397606cd9f"


def main() -> None:
    check_env()

    engine = create_engine(db_url)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    helper = TokenHelper(f"https://id.{env["INNET_HOST"]}", env["INNET_CLIENT_NAME"], env["INNET_CLIENT_SECRET"])

    # Get token and expiry date of token
    token, expires_at = helper.get_token()

    auth_header = {"Authorization": "Bearer " + token}
    response = requests.request("GET", f"https://meta.{env["INNET_HOST"]}/v1/site", headers=auth_header)

    print("META:")
    print(response.json())

    response = requests.request(
        "GET",
        f"https://data.{env["INNET_HOST"]}/v1/timeseries/measurements",
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
