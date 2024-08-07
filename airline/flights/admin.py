from django.contrib import admin

from .models import Flight, Airport, Passenger
# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    # Change the display of the admin site
    # Note that 'id', 'origin' etc are just names of the columns
    list_display = ('id', 'origin', 'destination', 'duration')

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger)

