from django.urls import path, include

from rest_framework.routers import DefaultRouter


from . import views


router = DefaultRouter()
router.register("sites", views.SiteViewSet)
router.register("devicemodels", views.DeviceModelViewSet)
router.register("loggers", views.LoggerViewSet)
router.register("installations", views.InstallationViewSet)
router.register("measurements", views.MeasurementViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("csrf/", views.get_csrf, name="api-csrf"),
    path("login/", views.login_view, name="api-login"),
    path("logout/", views.logout_view, name="api-logout"),
]
