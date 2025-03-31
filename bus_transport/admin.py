from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BusRoute, BusBooking

admin.site.register(BusRoute)
admin.site.register(BusBooking)
