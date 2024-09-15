"""API fetch script to add entries, run periodically"""

import requests

from db.env import env, check_env, db_url
from db.models import Site

from TokenHelper import TokenHelper

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def innet_main(session) -> None:
    """https://portal.dev.innet.io"""

    # Get auth token
    helper = TokenHelper(f"https://id.{env["INNET_HOST"]}", env["INNET_CLIENT_NAME"], env["INNET_CLIENT_SECRET"])
    token, expires_at = helper.get_token()
    auth_header = {"Authorization": "Bearer " + token}

    # Fetch list of sites
    sites = requests.request("GET", f"https://meta.{env["INNET_HOST"]}/v1/site", headers=auth_header, params={
        "project_id": env["INNET_PROJECT_ID"], # set in .env
        "exclude_historic": False,
        "exclude_prepared": False,
    })

    print("Sites:")
    for site in sites.json():
        print(site)

    return

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


if __name__ == "__main__":
    try:
        check_env()

        engine = create_engine(db_url)
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        innet_main(session)

        # # later: fetch data from other providers
        # meteoblue_main() # meteoblue https://measurements-api.meteoblue.com/v2/docs
        # ugz_internal_main()
    except Exception as e:
        print(f"An error occurred: {e}")
