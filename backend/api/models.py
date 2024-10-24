from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.dateparse import parse_datetime


class Organization(models.TextChoices):
    UGZ = "UGZ", "Umwelt- und Gesundheitsschutz Zürich"
    INNET = "INN", "INNET"
    METEOBLUE = "MET", "Meteoblue"
    AWEL = "AWE", "Amt für Abfall, Wasser, Energie und Luft"


# Mutations to a logger
class Actions(models.TextChoices):
    CAL = "CAL", "Calibration"
    PER = "PER", "Periodic Maintenance"
    FWU = "FWU", "Firmware Update"
    SRP = "SRP", "Sensor Replacement"
    BRP = "BRP", "Battery Replacement"
    DEX = "DEX", "Data Extraction"
    FRS = "FRS", "Factory Reset"
    INS = "INS", "Inspection"
    ENV = "ENV", "Environmental Adjustment"
    CLN = "CLN", "Cleaning"
    MOV = "MOV", "Moved"


class Site(models.Model):
    organization = models.CharField(
        max_length=3, choices=Organization.choices, default=Organization.UGZ
    )
    name = models.CharField(max_length=64, unique=True)
    wgs84_lat = models.DecimalField(max_digits=7, decimal_places=5)
    wgs84_lon = models.DecimalField(max_digits=7, decimal_places=5)
    masl = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} lat: {round(self.wgs84_lat, 2)} lon: {round(self.wgs84_lon, 2)} masl: {round(self.masl, 1)}"


class Technician(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(unique=True, max_length=254)
    description = models.CharField(max_length=256, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DeviceModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=128, default="")
    manufacturer_url = models.CharField(max_length=128, default="", blank=True)

    datasheet = models.FileField(upload_to="device-datasheets/", null=True, blank=True)
    user_manual = models.FileField(upload_to="device-user_manual/", null=True, blank=True)
    attachment = models.FileField(upload_to="device-attachments/", null=True, blank=True)
    image = models.ImageField(upload_to="device-images/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Logger(models.Model):
    sensor_id = models.CharField(unique=True, max_length=128)
    sensor_serial = models.CharField(max_length=128, null=True, blank=True)
    organization = models.CharField(
        max_length=3, choices=Organization.choices, default=Organization.UGZ
    )

    device_model = models.ForeignKey(DeviceModel, related_name="loggers", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sensor_id} ({self.device_model}) serial: {self.sensor_serial}"


class LoggerAction(models.Model):
    action = models.CharField(max_length=3, choices=Actions.choices, default=Actions.CAL)

    logger = models.ForeignKey(Logger, related_name="logger_actions", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sensor_id} ({self.device_model}) serial: {self.sensor_serial}"


class Installation(models.Model):
    interval_s = models.IntegerField(default=600, validators=[MinValueValidator(0)])
    notes = models.CharField(max_length=512, default="", blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to="installation-images/", null=True, blank=True)
    magl = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)], null=True, blank=True
    )

    site = models.ForeignKey(Site, related_name="installations", on_delete=models.CASCADE)
    logger = models.ForeignKey(Logger, related_name="installations", on_delete=models.CASCADE)
    technician = models.ForeignKey(
        Technician, related_name="installations", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end and self.start >= self.end:
            raise ValidationError("Start time must be earlier than end time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures validation rules from clean() are applied
        super().save(*args, **kwargs)

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

    installation = models.ForeignKey(
        Installation, related_name="measurements", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.timestamp = parse_datetime(self.timestamp)

        # Check if if the proposed measurement already exists in the database
        newer_measurements_exist = Measurement.objects.filter(
            installation=self.installation, meas_type=self.meas_type, timestamp__gte=self.timestamp
        ).exists()

        # Proceed with the save operation only if the measurement is actually new
        if not newer_measurements_exist:
            super(Measurement, self).save(*args, **kwargs)

    def __str__(self):
        f"{self.meas_type} {self.value} {self.timestamp}"
