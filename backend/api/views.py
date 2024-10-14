from rest_framework import viewsets

from api.models import Site, DeviceModel, Logger, Installation, Measurement

from .serializers import (
    SiteSerializer,
    DeviceModelSerializer,
    LoggerSerializer,
    InstallationSerializer,
    MeasurementSerializer,
)


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class DeviceModelViewSet(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer


class LoggerViewSet(viewsets.ModelViewSet):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class InstallationViewSet(viewsets.ModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
