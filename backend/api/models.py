from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.dateparse import parse_datetime


class Site(models.Model):
    class Providers(models.TextChoices):
        UGZ = "UGZ", "Umwelt- und Gesundheitsschutz Zürich"
        INNET = "INN", "INNET"
        METEOBLUE = "MET", "Meteoblue"
        AWEL = "AWE", "Amt für Abfall, Wasser, Energie und Luft"

    provider = models.CharField(max_length=3, choices=Providers.choices, default=Providers.UGZ)
    name = models.CharField(max_length=64, unique=True)
    wgs84_lat = models.DecimalField(max_digits=7, decimal_places=5)
    wgs84_lon = models.DecimalField(max_digits=7, decimal_places=5)
    masl = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    magl = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        null=True,
        default=None,
    )

    def __str__(self):
        return f"{self.name} lat: {round(self.wgs84_lat, 2)} lon: {round(self.wgs84_lon, 2)} masl: {round(self.masl, 1)}"


class DeviceModel(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=100)
    datasheet = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Logger(models.Model):
    sensor_id = models.CharField(primary_key=True, unique=True, max_length=100)
    sensor_serial = models.CharField(unique=True, max_length=100)

    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sensor_id} ({self.device_model}) serial: {self.sensor_serial} "


class Installation(models.Model):
    technician = models.CharField(max_length=20)
    interval_s = models.IntegerField(default=600, validators=[MinValueValidator(0)])
    notes = models.CharField(max_length=512, default="")
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    logger = models.ForeignKey(Logger, on_delete=models.CASCADE)

    def clean(self):
        if self.end and self.start >= self.end:
            raise ValidationError("Start time must be earlier than end time.")

    def __str__(self):
        return f"{self.site.name} {self.logger.device_model.name} {self.start} "


class Measurement(models.Model):
    class MeasurementType(models.TextChoices):
        # Source: https://static1.squarespace.com/static/597dc443914e6bed5fd30dcc/t/656d99b8f279294f7ab2db3a/1701681664838/MeteoHelix+IoT+Pro+DataSheet.pdf
        WIND_SPEED_MS = "ws_ms", "wind speed, ms^-1"
        WIND_SPEED_MAX_MS = "ws_max_ms", "max wind , ms^-1"
        EAST_WIND_SPEED_MS = "e_ws_ms", "east wind speed, ms^-1"
        NORTH_WIND_SPEED_MS = "n_ws_ms", "north wind speed, ms^-1"
        REL_HUMIDITY_PCT = "rel_h_pct", "humidity, percent"
        IRRADIATION_WM2 = "irr_wm2", "irradiation wm^-2"
        WIND_DIRECTION_DEG = "w_dir_deg", "wind direction, degrees"
        ATM_PRESSURE_HPA = "atm_p_hpa", "pressure, hPa"
        AIR_TEMPERATURE_C = "air_t_c", "temperature, C"
        BATTERY_VOLTAGE_V = "bat_v", "battery, V"
        PRECIPITATION_MM = "precip_mm", "precipitation, 10^-3m"
        DEWPOINT_C = "dewpoint_t_c", "Dew Point, C"
        GLOBAL_RADIATION_WM2 = "global_rad_wm2", "Solar Irradiation, Wm^-2"

    meas_type = models.CharField(max_length=16, choices=MeasurementType.choices)
    value = models.DecimalField(max_digits=10, decimal_places=5)
    timestamp = models.DateTimeField()

    installation = models.ForeignKey(Installation, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.timestamp = parse_datetime(self.timestamp)

        # Check if if the proposed measurement already exists in the database
        newer_measurements = Measurement.objects.filter(
            installation=self.installation, meas_type=self.meas_type, timestamp__gte=self.timestamp
        )

        # Proceed with the save operation only if the measurement is actually new
        if not len(newer_measurements):
            super(Measurement, self).save(*args, **kwargs)

    def __str__(self):
        f"{self.meas_type} {self.value} {self.timestamp}"
