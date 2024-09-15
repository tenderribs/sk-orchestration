"""API fetch script to add entries, run periodically"""

import requests

from db.env import env, check_env, db_url
from db.models import Site, Logger
from db.upsert import upsert_loggers, upsert_sites

from TokenHelper import TokenHelper

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session

# COOLDOWN_S = 1  # avoid HTTP 429s by waiting between requests


def refresh_innet_sites(session: session, auth_header: dict) -> None:
    """Get an updated list of sites"""
    sites = requests.request(
        "GET",
        f"https://meta.{env["INNET_HOST"]}/v1/site",
        headers=auth_header,
        params={
            "project_id": env["INNET_PROJECT_ID"],  # set in .env
            "exclude_historic": False,
            "exclude_prepared": False,
        },
    )

    upsert_sites(session, sites.json())


def fetch_active_site_data(
    session: session, auth_header: dict, active_sites: list[Site]
):
    for site in active_sites:
        # get the loggers related to each site
        logger_installations = requests.request(
            "GET",
            f"https://meta.{env["INNET_HOST"]}/v1/site/{site.id}/logger_installations",
            params={"site_id": site.id},
            headers=auth_header,
        )

        # then save the loggers in the DB
        upsert_loggers(session, logger_installations.json())

    loggers = session.query(Logger).filter_by(active=True).all()

    print("Fetching active loggers")

    for logger in loggers:
        data = requests.request(
            "GET",
            f"https://data.{env["INNET_HOST"]}/v1/timeseries/measurements",
            params={"logger_id": logger.id},
            headers=auth_header,
        )

        print(data.json(), "\n\n")


def innet_main(session: session) -> None:
    """https://portal.dev.innet.io"""

    # Get authentication token
    helper = TokenHelper(
        f"https://id.{env["INNET_HOST"]}",
        env["INNET_CLIENT_NAME"],
        env["INNET_CLIENT_SECRET"],
    )
    token, expires_at = (
        helper.get_token()
    )  # assume expiration long after script has finished executing
    auth_header = {"Authorization": "Bearer " + token}

    refresh_innet_sites(session, auth_header)

    active_sites: list(Site) = (
        session.query(Site).filter_by(provider_id="innet", active=True).all()
    )
    fetch_active_site_data(session, auth_header, active_sites)


if __name__ == "__main__":
    try:
        check_env()

        engine = create_engine(db_url)

        Session: sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
        session: session = Session()

        innet_main(session)

        # # later: fetch data from other providers
        # meteoblue_main() # meteoblue https://measurements-api.meteoblue.com/v2/docs
        # ugz_internal_main()
    except Exception as e:
        print(f"An error occurred: {e}")
