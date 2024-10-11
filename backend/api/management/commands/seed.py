import pandas as pd
import pytz

from pathlib import Path
from datetime import datetime

from api.models import Site, DeviceModel, Installation, Logger
from django.core.management.base import BaseCommand


# from https://github.com/perron2/lv95/blob/d04c92d94310da1a63bb6d18f49d62c0d7bae35e/lib/lv95.dart#L148
def lv95_to_wgs84(x: float, y: float):
    x1 = (x - 1200000) / 1000000
    x2 = x1 * x1
    x3 = x2 * x1

    y1 = (y - 2600000) / 1000000
    y2 = y1 * y1
    y3 = y2 * y1

    lat = (
        16.9023892 + 3.238272 * x1 - 0.270978 * y2 - 0.002528 * x2 - 0.0447 * y2 * x1 - 0.0140 * x3
    )
    lon = 2.6779094 + 4.728982 * y1 + 0.791484 * y1 * x1 + 0.1306 * y1 * x2 - 0.0436 * y3

    lat = lat * 100 / 36
    lon = lon * 100 / 36

    return lat, lon


class Command(BaseCommand):
    help = "Seed the database with data from a CSV file"

    def handle(self, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent

        ugz_awel = pd.read_csv(f"{BASE_DIR}/meta_aktive_awel+ugz.csv", sep=";")

        for index, row in ugz_awel.iterrows():
            # clean the sensor type's whitespace
            name = str(row["Sensortyp"]).replace(" ", "-")

            # create the Device Model based on listed types, overwriting duplicates
            dev_model, status = DeviceModel.objects.update_or_create(name=name)

            # create Loggers with listed ID and Serial data, overwriting duplicates
            logger, status = Logger.objects.update_or_create(
                sensor_id=row["SensorID"],
                defaults={
                    "sensor_serial": row["SensorSerial"],
                    "device_model": dev_model,
                },
            )

            # create Site and overwrite duplicates
            provider = "AWE" if "(AWEL)" in row["Name"] else "UGZ"
            lat, lon = lv95_to_wgs84(row["N"], row["E"])
            site, status = Site.objects.update_or_create(
                provider=provider,
                name=row["Name"],
                defaults={
                    "provider": provider,
                    "wgs84_lat": lat,
                    "wgs84_lon": lon,
                    "masl": row["masl"],
                },
            )

            # create Installation
            tz = pytz.timezone("Europe/Zurich")

            start = row["StartDatum"]
            start = tz.localize(datetime.strptime(start, "%d.%m.%Y %H:%M:%S")).strftime(
                "%Y-%m-%d %H:%M:%S %z"
            )

            end = None if "#" in row["EndDatum"] else row["EndDatum"]
            if end:
                end = tz.localize(datetime.strptime(end, "%d.%m.%Y %H:%M:%S")).strftime(
                    "%Y-%m-%d %H:%M:%S %z"
                )

            Installation.objects.create(
                technician=provider, start=start, end=end, site=site, logger=logger
            )

        self.stdout.write(self.style.SUCCESS("Data seeded successfully!"))
