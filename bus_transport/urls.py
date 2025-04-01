from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_buses, name='search_buses'),
    path('book/', views.book_bus, name='book_bus'),
    path('register/', views.register_bus_route, name='register_bus_route'),
]
