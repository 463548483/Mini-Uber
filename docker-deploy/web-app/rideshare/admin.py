from django.contrib import admin
from .models import Driver, sharer_search

from rideshare.models import Rides,Driver
# Register your models here.

admin.site.register(Rides)
admin.site.register(Driver)
admin.site.register(sharer_search)