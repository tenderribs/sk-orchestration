import pandas as pd
import pytz
import os


from pathlib import Path
from datetime import datetime
from requests import request


from api.models import Site, DeviceModel, Installation, Logger
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with data from a CSV file"

    BASE_DIR = Path(__file__).resolve().parent

    def lv95_to_wgs84(self, x: float, y: float):
        """
        from https://github.com/perron2/lv95/blob/d04c92d94310da1a63bb6d18f49d62c0d7bae35e/lib/lv95.dart#L148
        """

        x1 = (x - 1200000) / 1000000
        x2 = x1 * x1
        x3 = x2 * x1

        y1 = (y - 2600000) / 1000000
        y2 = y1 * y1
        y3 = y2 * y1

        lat = (
            16.9023892
            + 3.238272 * x1
            - 0.270978 * y2
            - 0.002528 * x2
            - 0.0447 * y2 * x1
            - 0.0140 * x3
        )
        lon = 2.6779094 + 4.728982 * y1 + 0.791484 * y1 * x1 + 0.1306 * y1 * x2 - 0.0436 * y3

        lat = lat * 100 / 36
        lon = lon * 100 / 36

        return lat, lon

    def format_datetime(self, datestring: str, in_fmt: str) -> str:
        """
        Explicitly localize the datestring as DST aware CEST datetime. Django DB layer saves
        it in UTC and exposes values as CEST.
        """

        out_tz = pytz.timezone("Europe/Zurich")
        out_fmt = "%Y-%m-%d %H:%M:%S %z"

        res = datetime.strptime(datestring, in_fmt)
        res = out_tz.localize(res).strftime(out_fmt)
        return res

    def import_ugz_awel(self):
        csv_df = pd.read_csv(f"{self.BASE_DIR}/meta_aktive_awel+ugz.csv", sep=";")
        csv_df = csv_df.dropna(
            subset=[
                "Sensortyp",
                "SensorID",
                "SensorSerial",
                "Name",
                "StartDatum",
            ]
        )

        def create_site(row: pd.DataFrame):
            """create Site and overwrite duplicates"""
            provider = "AWE" if "(AWEL)" in row["Name"] else "UGZ"
            lat, lon = self.lv95_to_wgs84(float(row["N"]), float(row["E"]))
            site, _ = Site.objects.update_or_create(
                provider=provider,
                name=row["Name"],
                defaults={
                    "provider": provider,
                    "wgs84_lat": round(lat, 5),
                    "wgs84_lon": round(lon, 5),
                    "masl": round(float(row["masl"]), 1),
                    "magl": round(float(row["magl"]), 1) if "#" not in row["magl"] else None,
                },
            )

            return site, provider

        def create_installation(row: pd.DataFrame, site, provider):
            """create Installation https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/#overview"""

            # localize start date
            start = self.format_datetime(row["StartDatum"], "%d.%m.%Y %H:%M:%S")

            # localize end date if available
            if "#" not in row["EndDatum"]:
                end = self.format_datetime(row["EndDatum"], "%d.%m.%Y %H:%M:%S")
            else:
                end = None

            Installation.objects.create(
                technician=provider,
                start=start,
                end=end,
                site=site,
                logger=logger,
                interval_s=600,
            )

        # Iterate over the CSV file rows
        for index, row in csv_df.iterrows():
            # clean the sensor type's whitespace
            name = str(row["Sensortyp"]).replace(" ", "-")

            # Create the Device Model
            dev_model, _ = DeviceModel.objects.update_or_create(name=name)

            # Create Loggers
            logger, _ = Logger.objects.update_or_create(
                sensor_id=row["SensorID"],
                defaults={
                    "sensor_serial": row["SensorSerial"],
                    "device_model": dev_model,
                },
            )

            # Create Site
            site, provider = create_site(row)

            # Create Installation
            create_installation(row, site, provider)

    def import_meteoblue_data(self):
        """
        Meteoblue has a really wacky CSV file with missing fields for their as well as an
        API endpoint with active stations.
        https://measurements-api.meteoblue.com/v2/baraniCityClimateZurich/station/get
        """

        # Group entries by site, dropping rows missing required information
        csv_df = pd.read_csv(
            f"{self.BASE_DIR}/Stationen_Zürich_Messnetz_meteoblue.csv", sep=","
        ).dropna(
            subset=[
                "sensor",
                "stationID",
                "latDecimal",
                "lonDecimal",
                "masl",
                "streetName",
                "installationDate",
            ]
        )

        def import_static_data(df: pd.DataFrame):
            # Prepare device models. provider barani is sensor "Barani" in meteoblue's CSV column, pessl is listed as "LoRain"
            lorain, _ = DeviceModel.objects.get_or_create(name="LoRain")
            barani, _ = DeviceModel.objects.get_or_create(name="Barani-Helix")

            for index, row in df.iterrows():
                # Site
                site, _ = Site.objects.update_or_create(
                    provider="MET",
                    name=row["streetName"],
                    defaults={
                        "provider": "MET",
                        "wgs84_lat": round(row["latDecimal"], 5),
                        "wgs84_lon": round(row["lonDecimal"], 5),
                        "masl": round(row["masl"], 1),
                        "magl": None,
                    },
                )

                # Logger
                device_model = barani if row["sensor"] == "Barani" else lorain
                logger, _ = Logger.objects.update_or_create(
                    sensor_id=row["stationID"],
                    sensor_serial=f"{device_model.name}_{row['stationID']}",
                    device_model=device_model,
                )

        def reconstruct_installations(df: pd.DataFrame):
            """
            Reconstruct installations history by visiting each location and checking the installed loggers
            assume old end == new start in the installationDate column
            """

            for street in df["streetName"].unique():
                # Sort entries corresponding to same site ascendingly
                entries = df[df["streetName"] == street].sort_values(
                    "installationDate", ascending=True
                )

                # The most recent installation has no end datetime and is currently active:
                most_recent = entries.iloc[-1]
                Installation.objects.create(
                    technician="MET",
                    interval_s=600,
                    notes=most_recent["notes"],
                    start=self.format_datetime(
                        most_recent["installationDate"], "%Y-%m-%d %H:%M:%S"
                    ),
                    end=None,
                    site=Site.objects.get(name=most_recent["streetName"]),
                    logger=Logger.objects.get(sensor_id=most_recent["stationID"]),
                )

                # For all entries preceding the most recent entry
                for index in range(entries.shape[0] - 1):  # iterate until most recent
                    curr_inst = entries.iloc[index]
                    next_inst = entries.iloc[index + 1]

                    start = self.format_datetime(curr_inst["installationDate"], "%Y-%m-%d %H:%M:%S")
                    end = self.format_datetime(next_inst["installationDate"], "%Y-%m-%d %H:%M:%S")

                    Installation.objects.create(
                        technician="MET",
                        interval_s=600,
                        notes=entries.iloc[index]["notes"],
                        start=start,
                        end=end,
                        site=Site.objects.get(name=curr_inst["streetName"]),
                        logger=Logger.objects.get(sensor_id=curr_inst["stationID"]),
                    )

        # Set up base information
        import_static_data(csv_df)

        # And reference base info when reconstructing installation history
        reconstruct_installations(csv_df)

    def import_innet_data(self):
        """
        Import INNET data.
        There are so few INNET objects that it is easiest to register manually
        """

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
            interval_s=600,
            site=vze_dach,
            logger=h766A,
        )
        Installation.objects.create(
            technician="INNET",
            start="2024-08-22 10:51:46 +02:00",
            end=None,
            interval_s=600,
            site=vze_dach,
            logger=b821E,
        )
        Installation.objects.create(
            technician="INNET",
            start="2024-08-22 10:51:22 +02:00",
            end=None,
            interval_s=600,
            site=vze_dach,
            logger=a3DD0,
        )
        Installation.objects.create(
            technician="INNET",
            start="2024-09-23 17:04:06 +02:00",
            end=None,
            interval_s=600,
            site=mel,
            logger=h86D6,
        )

    def handle(self, *args, **kwargs):
        self.import_ugz_awel()
        self.stdout.write(self.style.SUCCESS("UGZ / AWEL Data seeded"))

        self.import_innet_data()
        self.stdout.write(self.style.SUCCESS("INNET Data seeded"))

        self.import_meteoblue_data()
        self.stdout.write(self.style.SUCCESS("Meteoblue Data seeded"))
