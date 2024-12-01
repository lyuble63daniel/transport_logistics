from django.db import models
from django.contrib.auth.models import User
from django.db import models
# from .models import TransportRecord 
import uuid

class TransportRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add user association
    vehicle_id = models.CharField(max_length=50, unique=True)
    driver_name = models.CharField(max_length=100)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    cargo_description = models.TextField()
    destination = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vehicle_id} - {self.destination}"


class Parcel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add user association
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender_name = models.CharField(max_length=100)
    sender_mobile = models.CharField(max_length=15)  # Added sender mobile field
    sender_email = models.EmailField()              # Added sender email field
    receiver_name = models.CharField(max_length=100)
    receiver_mobile = models.CharField(max_length=15)  # Added receiver mobile field
    receiver_email = models.EmailField()              # Added receiver email field
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # in kilograms
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Shipped', 'Shipped'),
            ('In Transit', 'In Transit'),
            ('Delivered', 'Delivered'),
        ],
        default='Pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    transport_record = models.ForeignKey(
        'TransportRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='parcels'
    )

    def __str__(self):
        return f"Parcel {self.tracking_id} - {self.status}"

# class TransportRecord(models.Model):
#     vehicle_id = models.CharField(max_length=50, unique=True)
#     driver_name = models.CharField(max_length=100)
#     departure_date = models.DateField()
#     arrival_date = models.DateField()
#     cargo_description = models.TextField()
#     destination = models.CharField(max_length=200)

#     def __str__(self):
#         return f"{self.vehicle_id} - {self.destination}"




# ################ parsal model ###############



# import uuid

# class Parcel(models.Model):
#     tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     sender_name = models.CharField(max_length=100)
#     receiver_name = models.CharField(max_length=100)
#     origin = models.CharField(max_length=200)
#     destination = models.CharField(max_length=200)
#     weight = models.DecimalField(max_digits=6, decimal_places=2)  # in kilograms
#     status = models.CharField(
#         max_length=50,
#         choices=[
#             ('Pending', 'Pending'),
#             ('Shipped', 'Shipped'),
#             ('In Transit', 'In Transit'),
#             ('Delivered', 'Delivered'),
#         ],
#         default='Pending',
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Parcel {self.tracking_id} - {self.status}"