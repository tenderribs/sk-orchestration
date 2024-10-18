from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST, require_GET

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
    permission_classes = [StricterDjangoModelPermissions]

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


# For initial login, a CSRF token is required
@require_GET
def get_csrf(request: HttpRequest):
    response = JsonResponse({"detail": "CSRF cookie set"})
    response["X-CSRFToken"] = get_token(request)
    return response


@require_POST
def login_view(request: HttpRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if username is None or password is None:
        return JsonResponse({"detail": "Please provide username and password."}, status=422)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, status=400)

    login(request, user)
    return JsonResponse({"detail": "Successfully logged in."})


def logout_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."}, status=400)

    logout(request)
    return JsonResponse({"detail": "Successfully logged out."})


class CheckAuth(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        return JsonResponse({"detail": "You're Authenticated"})
