from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import BusRoute, BusBooking
from django.contrib import messages

def search_buses(request):
    routes = []

    if request.method == 'GET' and 'from' in request.GET and 'to' in request.GET:
        origin = request.GET.get('from')
        destination = request.GET.get('to')
        routes = BusRoute.objects.filter(origin__icontains=origin, destination__icontains=destination)

    return render(request, 'search_buses.html', {'routes': routes})


# def book_bus(request):
#     if request.method == 'POST':
#         route_id = request.POST.get('route_id')
#         name = request.POST.get('passenger_name')
#         seat = request.POST.get('seat_number')

#         try:
#             route = BusRoute.objects.get(id=route_id)
#             BusBooking.objects.create(
#                 route=route,
#                 passenger_name=name,
#                 seat_number=seat
#             )
#             messages.success(request, "✅ Booking successful!")
#         except:
#             messages.error(request, "❌ Booking failed. Try again.")

#     return redirect('search_buses')

from app.models import TransportRecord  # Replace 'app' with your actual app name


def book_bus(request):
    if request.method == 'POST':
        route_id = request.POST.get('route_id')
        name = request.POST.get('passenger_name')
        seat = request.POST.get('seat_number')

        try:
            route = BusRoute.objects.get(id=route_id)
            booking = BusBooking.objects.create(
                route=route,
                passenger_name=name,
                seat_number=seat
            )

            # ✅ Also create a transport record
            TransportRecord.objects.create(
                user=request.user,
                vehicle_id=f"BUS-{route.bus_number}-{seat}",
                driver_name="Bus Driver",  # or assign dynamically if you want
                departure_date=route.departure_time.date(),
                arrival_date=route.arrival_time.date(),
                cargo_description=f"Bus booking for {name}, Seat {seat}",
                destination=route.destination
            )

            messages.success(request, "✅ Booking successful and added to transport records!")
        except Exception as e:
            print("❌ Booking error:", e)
            messages.error(request, "❌ Booking failed. Try again.")

    return redirect('search_buses')