from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions


from api.models import Site, DeviceModel, Logger, Installation, Measurement

from .serializers import (
    SiteSerializer,
    DeviceModelSerializer,
    LoggerSerializer,
    InstallationSerializer,
    MeasurementSerializer,
)


class StricterDjangoModelPermissions(DjangoModelPermissions):
    # Add 'view' permission for GET requests. Authentication is required by default
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class SiteViewSet(viewsets.ModelViewSet):
    permission_classes = []

    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class DeviceModelViewSet(viewsets.ModelViewSet):
    permission_classes = [StricterDjangoModelPermissions]

    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer


class LoggerViewSet(viewsets.ModelViewSet):
    permission_classes = [StricterDjangoModelPermissions]

    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class InstallationViewSet(viewsets.ModelViewSet):
    permission_classes = [StricterDjangoModelPermissions]

    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    permission_classes = [StricterDjangoModelPermissions]

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
