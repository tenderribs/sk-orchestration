from api.models import Site, DeviceModel, Logger, Installation, Measurement
from django.contrib.auth.models import User
from rest_framework import serializers


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class LoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logger
        fields = "__all__"


class DeviceModelSerializer(serializers.ModelSerializer):
    loggers = LoggerSerializer(many=True)

    class Meta:
        model = DeviceModel
        fields = ["name", "datasheet", "loggers"]


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
