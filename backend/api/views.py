from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from api.models import Site, DeviceModel, Logger, Installation, Measurement

from .serializers import (
    SiteSerializer,
    DeviceModelSerializer,
    LoggerSerializer,
    InstallationSerializer,
    MeasurementSerializer,
)


class SiteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class DeviceModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer


class LoggerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class InstallationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
