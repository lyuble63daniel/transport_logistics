from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_flights, name='search_flights'),
    path('import/', views.import_flight, name='import_flight'),
]
