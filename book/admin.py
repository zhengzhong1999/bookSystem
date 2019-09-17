from django.contrib import admin
from book.models import Flight, Customer,Payment
from .forms import FlightForm

class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'departure_city', 'arrive_city', 'departure_airport', 'arrive_airport', 'departure_time', 'arrive_time', 'capacity',
        'first_capacity','price', 'book_sum','first_price','first_book_sum')
    form = FlightForm

# Register your models here.

admin.site.register(Flight,FlightAdmin)


