from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transport/create/', views.create_transport, name='create_transport'),
    path('transport/', views.list_transport, name='list_transport'),
    path('transport/update/<int:id>/', views.update_transport, name='update_transport'),
    path('transport/delete/<int:id>/', views.delete_transport, name='delete_transport'),
    path('parcel/create/', views.create_parcel, name='create_parcel'),
    path('parcel/track/', views.track_parcel, name='track_parcel'),
    path('parcel/update/<uuid:tracking_id>/', views.update_parcel, name='update_parcel'),
    path('parcel/list/', views.list_parcels, name='list_parcels'),
    path('public/track/', views.public_track_parcel, name='public_track_parcel'),
    path('parcel/delete/<uuid:tracking_id>/', views.delete_parcel, name='delete_parcel'),
    path('contact/', views.contact_us, name='contact_us'),
    path('', views.user_home, name='user_home'),
    path("calculate-shipping/", views.calculate_shipping_view, name="calculate_shipping"),

]
