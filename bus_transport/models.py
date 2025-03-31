from django.db import models

# Create your models here.
from django.db import models

class BusRoute(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    bus_number = models.CharField(max_length=50)
    fare = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.bus_number}: {self.origin} → {self.destination}"

class BusBooking(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    seat_number = models.CharField(max_length=10)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger_name} - {self.route.bus_number} - Seat {self.seat_number}"
