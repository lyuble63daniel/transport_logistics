from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_buses, name='search_buses'),
    path('book/', views.book_bus, name='book_bus'),
]
