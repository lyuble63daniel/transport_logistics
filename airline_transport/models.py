from django.db import models

# Create your models here.
from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.flight_number} ({self.origin} → {self.destination})"
