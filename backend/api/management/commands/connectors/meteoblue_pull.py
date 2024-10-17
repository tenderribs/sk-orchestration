"""INNET API fetch script to inject latest data into UGZ backend"""

import pandas as pd
import pytz

from requests import request
from datetime import datetime
from os import environ as env

from api.models import Installation, Measurement


targets = {
    "LoRain": {
        "fields": ["airTemperature", "precipitation", "relativeHumidity", "battery"],
        "project": "pesslCityClimateZurich",
    },
    "Barani-Helix": {
        "fields": [
            "airTemperature",
            "relativeHumidity",
            "globalRadiation",
            "pressure_sfc",
            "battery",
        ],
        "project": "baraniCityClimateZurich",
    },
}


meas_types = {
    "airTemperature": "air_t_c",
    "precipitation": "precip_mm",
    "battery": "bat_v",
    "relativeHumidity": "rel_h_pct",
    "dewPoint": "dewpoint_t_c",
    "globalRadiation": "global_rad_wm2",
    "pressure_sfc": "atm_p_hpa",
}


def localize(unix_time: int) -> str:
    dt = datetime.utcfromtimestamp(unix_time)
    local_dt = pytz.timezone("Europe/Zurich").localize(dt)
    return local_dt.strftime("%Y-%m-%d %H:%M:%S %z")


def execute_query(project, params) -> pd.DataFrame:
    res: dict = request(
        "GET",
        url=f"https://measurements-api.meteoblue.com/v2/{project}/raw/measurement/get",
        params=params,
    ).json()

    if "columns" not in res:
        raise ValueError("No data columns in response")

    data = {entry["column"]: entry["values"] for entry in res["columns"]}
    df = pd.DataFrame().from_dict(data)

    # Cast unix time to localized timestamp in Europe/Zurich TZ
    df["timestamp"] = df["timestamp"].apply(localize)

    return df


def main():
    auth_params = {"apikey": env["METEOBLUE_SECRET"]}

    for device, params in targets.items():
        # Get all active installations per device type
        installations = Installation.objects.filter(
            end=None, logger__device_model__name=device, site__provider="MET"
        )

        print(f"Querying Meteoblue API for {len(installations)} {device} devices")

        # Prepare query parameters
        project = params["project"]
        data_fields = params["fields"]
        stations = [installation.logger.sensor_id for installation in installations]

        query_params = {
            "latest": True,
            "fields": ["id", "timestamp", *data_fields],  # ignore asl, lat, lon
            "stations": stations,
            "limit": len(installations),  # load precise number of rows for each installation
        }

        # Execute the query
        df: pd.DatFrame = execute_query(project=project, params={**auth_params, **query_params})

        for index, row in df.iterrows():
            for column, meas_type in meas_types.items():
                if column in row and pd.notna(row[column]):
                    Measurement.objects.create(
                        meas_type=meas_type,
                        value=row[column],
                        timestamp=row["timestamp"],
                        installation=installations.get(logger__sensor_id=row["id"]),
                    )
