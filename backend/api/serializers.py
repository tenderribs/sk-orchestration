from api.models import Site, DeviceModel, Logger, Installation, Measurement
from django.contrib.auth.models import User
from rest_framework import serializers


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class DeviceModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceModel
        fields = "__all__"


class LoggerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Logger
        fields = "__all__"


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class InstallationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Installation
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
