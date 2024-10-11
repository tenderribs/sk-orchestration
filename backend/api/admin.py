from django.contrib import admin

# Register your models here.
from .models import Site, DeviceModel, Logger, Installation, Measurement

admin.site.register(Site)
admin.site.register(DeviceModel)
admin.site.register(Logger)
admin.site.register(Installation)
admin.site.register(Measurement)
