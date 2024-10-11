from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import (
    SiteViewSet,
    DeviceModelViewSet,
    LoggerViewSet,
    InstallationViewSet,
    MeasurementViewSet,
)

router = DefaultRouter()
router.register("sites", SiteViewSet)
router.register("devicemodels", DeviceModelViewSet)
router.register("loggers", LoggerViewSet)
router.register("installations", InstallationViewSet)
router.register("measurements", MeasurementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
