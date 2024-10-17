"""INNET API fetch script to inject latest data into UGZ backend"""

from requests import request
from os import environ as env

from api.models import Installation, Measurement
from .TokenHelper import TokenHelper


def fetch_auth_headers():
    """Get header w/ authentication token"""

    helper = TokenHelper(
        f"https://id.{env['INNET_HOST']}",
        env["INNET_CLIENT_NAME"],
        env["INNET_CLIENT_SECRET"],
    )

    token, expires_at = helper.get_token()

    # Assume script execution complete before INNET token expiry
    return {"Authorization": "Bearer " + token}


field_mapping = {
    "DL-BLG": [
        {"type": "bat_v", "field": "%SERIAL%.battery.V"},
        {"type": "t_c", "field": "%SERIAL%.globe-temperature.C"},
        {"type": "t_c", "field": "%SERIAL%.temperature.C"},
    ],
    "DL-Atmos-22": [
        {"type": "t_c", "field": "%SERIAL%.temperature.C"},
        {"type": "w_dir_deg", "field": "%SERIAL%.wdir.deg"},
        {"type": "ws_max_ms", "field": "%SERIAL%.wspd_max.ms"},
        {"type": "ws_ms", "field": "%SERIAL%.wspd.ms"},
    ],
    "Barani-Helix": [
        {"type": "p_hpa", "field": "%SERIAL%.pressure.hpa"},
        {"type": "t_c", "field": "%SERIAL%.temperature.C"},
        {"type": "irr_wm2", "field": "%SERIAL%.irradiation.wm2"},
        {"type": "h_pct", "field": "%SERIAL%.humidity.pct"},
    ],
}


def query_innet(headers: dict, deveui: str, field_name: str):
    """Query INNET REST API for selected loggers' sensor types"""

    data = request(
        "GET",
        f"https://data.{env['INNET_HOST']}/v1/timeseries/{field_name}/last_records",
        params={
            "logger_id": deveui,
            "record_count": 1,
            "field": "final",
            "validity": "valid",
        },
        headers=headers,
    ).json()

    if "values" not in data or not isinstance(data["values"], list) or not len(data["values"]):
        raise ValueError("Measurement has no value")

    if (
        "timestamps" not in data
        or not isinstance(data["timestamps"], list)
        or not len(data["timestamps"])
    ):
        raise ValueError("Measurement has no timestamp")

    return data["values"][0], data["timestamps"][0]


def main():
    auth_headers = fetch_auth_headers()

    # Active INNET installations
    installations = Installation.objects.filter(end=None, site__provider="INN")

    for installation in installations:
        deveui = installation.logger.sensor_id
        sensor_serial = installation.logger.sensor_serial
        sensor_type = installation.logger.device_model.name

        print(f"\n\nFetching latest data for logger {sensor_serial} (deveui {deveui})")

        # Get the correspondence between a device model and the fields offered by INNET
        mapping = field_mapping[sensor_type]

        for fm in mapping:
            meas_type, field_name = (
                fm["type"],
                fm["field"].replace("%SERIAL%", sensor_serial),
            )

            print(f"Querying {field_name}")

            try:
                value, timestamp = query_innet(
                    headers=auth_headers, deveui=deveui, field_name=field_name
                )

                Measurement.objects.create(
                    meas_type=meas_type, value=value, timestamp=timestamp, installation=installation
                )

                print(f"{meas_type} \t {round(value, 2)} \t {timestamp}")

            except Exception as e:
                print(f"Couldn't add {field_name}, ignoring ({e})")
