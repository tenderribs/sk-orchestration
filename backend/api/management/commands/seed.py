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

    BASE_DIR = Path(__file__).resolve().parent

    def handle_ugz_awel(self):
        df = pd.read_csv(f"{self.BASE_DIR}/meta_aktive_awel+ugz.csv", sep=";")

        for index, row in df.iterrows():
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
                    "wgs84_lat": round(lat, 5),
                    "wgs84_lon": round(lon, 5),
                    "masl": round(row["masl"], 1),
                },
            )

            # create Installation
            # https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/#overview
            tz = pytz.timezone("Europe/Zurich")
            in_fmt = "%d.%m.%Y %H:%M:%S"
            out_fmt = "%Y-%m-%d %H:%M:%S %z"

            # localize start date
            start = datetime.strptime(row["StartDatum"], in_fmt)
            start = tz.localize(start).strftime(out_fmt)

            # localize end date if available
            if "#" not in row["EndDatum"]:
                end = datetime.strptime(row["EndDatum"], in_fmt)
                end = tz.localize(end).strftime(out_fmt)
            else:
                end = None

            Installation.objects.create(
                technician=provider, start=start, end=end, site=site, logger=logger
            )

    # Currently Meteoblue isn't supported because it has a really wacky CSV file with missing fields
    def handle_meteoblue_data(self):
        df = pd.read_csv(f"{self.BASE_DIR}/Stationen_Zürich_Messnetz_meteoblue.csv", sep=",")

        # Save all the stations that are supposedly doing ok
        for index, row in df[df["functionCheck"] == "ok"].iterrows():
            device_model, status = DeviceModel.objects.update_or_create(name=row["sensor"])

            logger, status = Logger.objects.update_or_create(
                sensor_id=row["stationID"], sensor_serial=str(index), device_model=device_model
            )

            site, status = Site.objects.update_or_create(
                provider="MET",
                name=row["streetName"],
                defaults={
                    "provider": "MET",
                    "wgs84_lat": round(row["latDecimal"], 5),
                    "wgs84_lon": round(row["lonDecimal"], 5),
                    "masl": round(row["masl"], 1),
                },
            )

    def handle_innet_data(self):
        helix = DeviceModel.objects.get(name="Barani-Helix")
        blg = DeviceModel.objects.get(name="DL-BLG")
        atm22 = DeviceModel.objects.get(name="DL-Atmos-22")

        h766A = Logger.objects.create(
            sensor_id="0004A30B00F7766A", sensor_serial="BDHEL017", device_model=helix
        )
        b821E = Logger.objects.create(
            sensor_id="0004A30B0105821E", sensor_serial="DLBLG001", device_model=blg
        )
        a3DD0 = Logger.objects.create(
            sensor_id="70B3D57BA0003DD0", sensor_serial="DLATM22001", device_model=atm22
        )
        h86D6 = Logger.objects.create(
            sensor_id="0004A30B00F786D6", sensor_serial="BDHEL026", device_model=helix
        )

        mel = Site.objects.create(
            provider="INN",
            name="Büro MEL 5. OG VZE",
            wgs84_lat=47.41605,
            wgs84_lon=8.54310,
            masl=439,
        )

        vze_dach = Site.objects.create(
            provider="INN",
            name="VZE Dach Referenzstation",
            wgs84_lat=47.41588,
            wgs84_lon=8.54206,
            masl=439,
        )

        Installation.objects.create(
            technician="INNET",
            start="2024-08-22 10:50:45 +02:00",
            end=None,
            site=vze_dach,
            logger=h766A,
        )
        Installation.objects.create(
            technician="INNET",
            start="2024-08-22 10:51:46 +02:00",
            end=None,
            site=vze_dach,
            logger=b821E,
        )
        Installation.objects.create(
            technician="INNET",
            start="2024-08-22 10:51:22 +02:00",
            end=None,
            site=vze_dach,
            logger=a3DD0,
        )
        Installation.objects.create(
            technician="INNET",
            start="2024-09-23 17:04:06 +02:00",
            end=None,
            site=mel,
            logger=h86D6,
        )

    def handle(self, *args, **kwargs):
        self.handle_ugz_awel()
        self.stdout.write(self.style.SUCCESS("UGZ / AWEL Data seeded successfully!"))

        # example DETAIL:  Key (sensor_id)=(034000CD) already exists
        # self.handle_meteoblue_data()
        # self.stdout.write(self.style.SUCCESS("Meteoblue Data seeded successfully!"))

        self.handle_innet_data()
        self.stdout.write(self.style.SUCCESS("INNET Data seeded successfully!"))
