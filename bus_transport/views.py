from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import BusRoute, BusBooking
from django.contrib import messages


import requests
from django.shortcuts import render, redirect
from django.contrib import messages

import requests
from django.shortcuts import render, redirect
from django.contrib import messages

def search_buses(request):
    routes = []
    if request.method == 'GET' and 'from' in request.GET and 'to' in request.GET:
        from_city = request.GET.get('from')
        to_city = request.GET.get('to')
        try:
            # ✅ Use your new FastAPI microservice (running locally or on a server)
            url = f"https://m97ksfo27c.execute-api.eu-west-1.amazonaws.com/lyuble/bus/search?from_city={from_city}&to_city={to_city}"
            response = requests.get(url)
            if response.status_code == 200:
                routes = response.json()
            else:
                messages.error(request, "❌ Failed to fetch bus routes.")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")

    return render(request, 'search_buses.html', {'routes': routes})


from app.models import TransportRecord  # Replace 'app' with your actual app name

from django.views.decorators.csrf import csrf_exempt

from app.models import TransportRecord
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required


@login_required
@csrf_exempt
def book_bus(request):
    if request.method == 'POST':
        route_id = request.POST.get('route_id')
        passenger_name = request.POST.get('passenger_name')
        seat_number = request.POST.get('seat_number')

        # Send booking request to FastAPI
        payload = {
            "route_id": route_id,
            "passenger_name": passenger_name,
            "seat_number": seat_number
        }

        try:
            api_response = requests.post("https://m97ksfo27c.execute-api.eu-west-1.amazonaws.com/lyuble/bus/book", json=payload)
            if api_response.status_code == 200:
                # ✅ Also fetch bus route details from FastAPI to store in TransportRecord
                print("post successfull")
                print(route_id)
                route_response = requests.get(f"https://m97ksfo27c.execute-api.eu-west-1.amazonaws.com/lyuble/bus/route/{route_id}")
                if route_response.status_code == 200:
                    print("route successfull")
                    route = route_response.json()

                    # ✅ Create a TransportRecord
                    TransportRecord.objects.create(
                        user=request.user,
                        vehicle_id=route['bus_number'],
                        driver_name=passenger_name,
                        departure_date=parse_datetime(route['departure_time']),
                        arrival_date=parse_datetime(route['arrival_time']),
                        cargo_description=f"Seat: {seat_number}",
                        destination=route['destination']
                    )

                    messages.success(request, "✅ Booking and record created!")
                else:
                    messages.warning(request, "Booking done, but couldn't fetch route for record.")
            else:
                messages.error(request, "❌ Booking failed.")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")

    return redirect('search_buses')





# def book_bus(request):
#     if request.method == 'POST':
#         route_id = request.POST.get('route_id')
#         name = request.POST.get('passenger_name')
#         seat = request.POST.get('seat_number')

#         try:
#             route = BusRoute.objects.get(id=route_id)
#             booking = BusBooking.objects.create(
#                 route=route,
#                 passenger_name=name,
#                 seat_number=seat
#             )

#             # ✅ Also create a transport record
#             TransportRecord.objects.create(
#                 user=request.user,
#                 vehicle_id=f"BUS-{route.bus_number}-{seat}",
#                 driver_name="Bus Driver",  # or assign dynamically if you want
#                 departure_date=route.departure_time.date(),
#                 arrival_date=route.arrival_time.date(),
#                 cargo_description=f"Bus booking for {name}, Seat {seat}",
#                 destination=route.destination
#             )

#             messages.success(request, "✅ Booking successful and added to transport records!")
#         except Exception as e:
#             print("❌ Booking error:", e)
#             messages.error(request, "❌ Booking failed. Try again.")

#     return redirect('search_buses')





from .forms import BusRouteForm
import requests
from uuid import uuid4
from django.contrib import messages

@login_required
def register_bus_route(request):
    if request.method == 'POST':
        form = BusRouteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            route_data = {
                "id": str(uuid4()),
                "origin": data['origin'],
                "destination": data['destination'],
                "departure_time": data['departure_time'].isoformat(),
                "arrival_time": data['arrival_time'].isoformat(),
                "bus_number": data['bus_number'],
                "fare": data['fare'],
            }

            try:
                response = requests.post("https://m97ksfo27c.execute-api.eu-west-1.amazonaws.com/lyuble/bus/routes", json=route_data)
                if response.status_code == 200:
                    messages.success(request, "✅ Bus route registered successfully!")
                    return redirect('dashboard')
                else:
                    messages.error(request, "❌ Failed to register route.")
            except Exception as e:
                messages.error(request, f"❌ Error: {str(e)}")
    else:
        form = BusRouteForm()

    return render(request, 'register_bus_route.html', {'form': form})