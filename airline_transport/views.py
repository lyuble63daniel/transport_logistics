from django.shortcuts import render

from app.models import TransportRecord  # ✅ correct
from .models import Flight
from django.contrib.auth.models import User  # If not already imported

# # Create your views here.

from django.views.decorators.http import require_POST
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
from .models import Flight
from django.contrib import messages

def search_flights(request):
    flights = []
    if request.method == 'GET' and 'from' in request.GET and 'to' in request.GET:
        from_city = request.GET.get('from')
        to_city = request.GET.get('to')
        api_url = f"http://airlinebusbooking-backend-lb-1215843260.eu-west-1.elb.amazonaws.com/api/airline/search-combined/?from={from_city}&to={to_city}"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                flights = data.get('flights', [])  # ✅ only get the flights key
            else:
                messages.error(request, "Failed to fetch flights.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'search_flights.html', {'flights': flights})

# @require_POST
# def import_flight(request):
#     data = request.POST
#     flight = Flight.objects.create(
#         flight_number=data.get('flight_number'),
#         origin=data.get('origin'),
#         destination=data.get('destination'),
#         departure_time=data.get('departure_time'),
#         arrival_time=data.get('arrival_time'),
#         airline_name=data.get('airline'),  # ✅ fix this line
#     )
#     return JsonResponse({'status': 'success', 'flight_id': flight.id})

@require_POST
def import_flight(request):
    try:
        data = request.POST

        flight = Flight.objects.create(
            flight_number=data.get('flight_number'),
            origin=data.get('origin'),
            destination=data.get('destination'),
            departure_time=data.get('departure_time'),
            arrival_time=data.get('arrival_time'),
            airline_name=data.get('airline'),
        )

        # Create matching transport record
        TransportRecord.objects.create(
            user=request.user,
            vehicle_id=f"FLIGHT-{flight.flight_number}",  # To keep it unique
            driver_name=flight.airline_name,
            departure_date=flight.departure_time[:10],  # Date only
            arrival_date=flight.arrival_time[:10],      # Date only
            cargo_description=f"Imported flight from {flight.origin} to {flight.destination}",
            destination=flight.destination,
        )

        return JsonResponse({'status': 'success', 'flight_id': flight.id})

    except Exception as e:
        print("❌ Import error:", e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
