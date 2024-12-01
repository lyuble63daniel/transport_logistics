from django.shortcuts import render, redirect, get_object_or_404
from .models import TransportRecord
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Parcel
import time
from shipping_cost_calculator import ShippingCostCalculator # import library


# library use
def calculate_shipping_view(request):
    if request.method == "POST":
        weight = float(request.POST.get("weight"))
        distance = float(request.POST.get("distance"))
        priority = request.POST.get("priority") == "on"
        fragile = request.POST.get("fragile") == "on"

        # Initialize the calculator
        calculator = ShippingCostCalculator()
        cost = calculator.calculate_cost(weight, distance, priority, fragile)

        messages.success(request, f"Shipping cost calculated: ${cost}")
        return redirect("calculate_shipping")

    return render(request, "calculate_shipping.html")

# Sign-up view
# Sign-up view

# Sign-up view
# Sign-up view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! Redirecting to login...")
            return render(request, 'signup.html', {'redirect_to_login': True})  # Pass flag for redirection
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('signup')

    return render(request, 'signup.html')

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         # Validate passwords
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match!")
#             return redirect('signup')

#         # Check if username already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists!")
#             return redirect('signup')

#         # Create the user
#         try:
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.save()
#             messages.success(request, "Account created successfully! Please log in.")
#             return redirect('login')
#         except Exception as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('signup')

#     return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")  # This is the Optional feedback message
    return redirect('user_home')  # This will Redirect to login after logging out,because When a user logs out, the typical flow is to redirect them to the login page. This makes sense because they will need to log in again to access the application

# Protected dashboard view
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})



########### CRUD ###############



# Create a transport record

@login_required
def list_transport(request):
    records = TransportRecord.objects.filter(user=request.user)  # Filter by user
    return render(request, 'list_transport.html', {'records': records})

@login_required
def create_transport(request):
    if request.method == 'POST':
        vehicle_id = request.POST['vehicle_id']
        driver_name = request.POST['driver_name']
        departure_date = request.POST['departure_date']
        arrival_date = request.POST['arrival_date']
        cargo_description = request.POST['cargo_description']
        destination = request.POST['destination']

        TransportRecord.objects.create(
            user=request.user,  # Associate record with the logged-in user
            vehicle_id=vehicle_id,
            driver_name=driver_name,
            departure_date=departure_date,
            arrival_date=arrival_date,
            cargo_description=cargo_description,
            destination=destination,
        )
        messages.success(request, "Transport record created successfully!")
        return redirect('list_transport')

    return render(request, 'create_transport.html')


# Update a transport record

@login_required
def update_transport(request, id):
    record = get_object_or_404(TransportRecord, id=id)
    if request.method == 'POST':
        record.vehicle_id = request.POST['vehicle_id']
        record.driver_name = request.POST['driver_name']
        record.departure_date = request.POST['departure_date']
        record.arrival_date = request.POST['arrival_date']
        record.cargo_description = request.POST['cargo_description']
        record.destination = request.POST['destination']
        record.save()
        messages.success(request, "Record updated successfully!")
        return redirect('list_transport')

    return render(request, 'update_transport.html', {'record': record})

# @login_required
# def update_transport(request, id):
#     record = get_object_or_404(TransportRecord, id=id)
#     if request.method == 'POST':
#         record.vehicle_id = request.POST['vehicle_id']
#         record.driver_name = request.POST['driver_name']
#         record.departure_date = request.POST['departure_date']
#         record.arrival_date = request.POST['arrival_date']
#         record.cargo_description = request.POST['cargo_description']
#         record.destination = request.POST['destination']
#         record.save()
#         messages.success(request, "Transport record updated successfully!")
#         return redirect('list_transport')

#     return render(request, 'update_transport.html', {'record': record})

# # Delete a transport record
# @login_required
# def delete_transport(request, id):
#     record = get_object_or_404(TransportRecord, id=id)
#     record.delete()
#     messages.success(request, "Transport record deleted successfully!")
#     return redirect('list_transport')

@login_required
def delete_transport(request, id):
    record = get_object_or_404(TransportRecord, id=id)
    record.delete()
    messages.success(request, "Record deleted successfully!")
    return redirect('list_transport')



##############################################################

#############  Parcel ##################
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from uuid import UUID




# ## Trac parcel ##


@login_required
def track_parcel(request):
    tracking_id = request.GET.get('tracking_id')
    parcel = None

    if tracking_id:
        try:
            # Validate tracking_id as a valid UUID
            uuid_obj = UUID(tracking_id, version=4)
            parcel = Parcel.objects.get(tracking_id=uuid_obj)
        except ValueError:
            # Handle invalid UUID format
            messages.error(request, _("Invalid Tracking ID format. Please enter a valid UUID."))
        except Parcel.DoesNotExist:
            # Handle valid UUID but no parcel found
            messages.error(request, _("No parcel found with the provided Tracking ID."))
        except ValidationError:
            messages.error(request, _("Invalid Tracking ID format. Please enter a valid UUID."))

    return render(request, 'track_parcel.html', {'parcel': parcel})
# @login_required
# def track_parcel(request):
#     tracking_id = request.GET.get('tracking_id')
#     parcel = None

#     if tracking_id:
#         try:
#             # Validate tracking_id as a valid UUID
#             uuid_obj = UUID(tracking_id, version=4)
#             parcel = Parcel.objects.get(tracking_id=uuid_obj)
#         except ValueError:
#             # Handle invalid UUID format
#             messages.error(request, _("Invalid Tracking ID format. Please enter a valid UUID."))
#         except Parcel.DoesNotExist:
#             # Handle valid UUID but no parcel found
#             messages.error(request, _("No parcel found with the provided Tracking ID."))
#         except ValidationError:
#             messages.error(request, _("Invalid Tracking ID format. Please enter a valid UUID."))

#     return render(request, 'track_parcel.html', {'parcel': parcel})
# @login_required
# def track_parcel(request):
#     tracking_id = request.GET.get('tracking_id')
#     parcel = None

#     if tracking_id:
#         try:
#             parcel = Parcel.objects.get(tracking_id=tracking_id)
#         except Parcel.DoesNotExist:
#             messages.error(request, "Invalid Tracking ID")

#     return render(request, 'track_parcel.html', {'parcel': parcel})

@login_required
def delete_parcel(request, tracking_id):
    if request.method == "POST":
        parcel = get_object_or_404(Parcel, tracking_id=tracking_id, user=request.user)
        parcel.delete()
        messages.success(request, "Parcel deleted successfully!")
        return redirect('list_parcels')
    return redirect('list_parcels')

@login_required
def list_parcels(request):
    parcels = Parcel.objects.filter(user=request.user)  # Filter by user
    return render(request, 'list_parcels.html', {'parcels': parcels})

# @login_required
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Process the form data (e.g., send an email, save to database, etc.)
        # For now, we are just simulating a successful submission
        messages.success(request, "Your message has been sent successfully!")
        return render(request, 'contact_us.html')  # Re-render the form page with success message
    
    return render(request, 'contact_us.html')


import boto3
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Parcel, TransportRecord


@login_required
def create_parcel(request):
    signup_link = f"{request.build_absolute_uri('/')}"
    if request.method == 'POST':
        sender_name = request.POST['sender_name']
        sender_mobile = request.POST['sender_mobile']
        sender_email = request.POST['sender_email']
        receiver_name = request.POST['receiver_name']
        receiver_mobile = request.POST['receiver_mobile']
        receiver_email = request.POST['receiver_email']
        origin = request.POST['origin']
        destination = request.POST['destination']
        weight = request.POST['weight']
        transport_record_id = request.POST.get('transport_record')

        # Fetch the transport record (if selected)
        transport_record = None
        if transport_record_id:
            try:
                transport_record = TransportRecord.objects.get(id=transport_record_id, user=request.user)
            except TransportRecord.DoesNotExist:
                messages.error(request, "Invalid transport record selected.")
                return redirect('create_parcel')

        # Create the parcel
        parcel = Parcel.objects.create(
            user=request.user,  # Associate parcel with the logged-in user
            sender_name=sender_name,
            sender_mobile=sender_mobile,
            sender_email=sender_email,
            receiver_name=receiver_name,
            receiver_mobile=receiver_mobile,
            receiver_email=receiver_email,
            origin=origin,
            destination=destination,
            weight=weight,
            transport_record=transport_record,  # Link the transport record
        )
        tracking_url = f"{signup_link}public/track/"
        # Prepare notification details
        message = f"""
Parcel Details:


Sender: {parcel.sender_name}
Mobile: {parcel.sender_mobile}
Email: {parcel.sender_email}

Receiver: {parcel.receiver_name}
Mobile: {parcel.receiver_mobile}
Email: {parcel.receiver_email}

Origin: {parcel.origin}
Destination: {parcel.destination}

Status: {parcel.status}

Assigned Vehicle:
Vehicle ID: {parcel.transport_record.vehicle_id if parcel.transport_record else 'Not Assigned'}
Destination: {parcel.transport_record.destination if parcel.transport_record else 'Not Assigned'}
Driver Name: {parcel.transport_record.driver_name if parcel.transport_record else 'Not Assigned'}
Departure Date: {parcel.transport_record.departure_date.strftime('%b. %d, %Y') if parcel.transport_record else 'Not Assigned'}
Arrival Date: {parcel.transport_record.arrival_date.strftime('%b. %d, %Y') if parcel.transport_record else 'Not Assigned'}

##################################################################

Tracking ID: {parcel.tracking_id}
To track the parcel, go to the following URL: {tracking_url}

##################################################################
"""

        # Publish the notification to SNS
        sns_client = boto3.client(
            'sns',
            region_name=settings.AWS_REGION,
            # aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            # aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            # aws_session_token=settings.AWS_SESSION_TOKEN
        )
        topic_arn = settings.AWS_SNS_TOPIC_ARN

        try:
            # Subscribe sender and receiver (if not already subscribed)
            for email in [parcel.sender_email, parcel.receiver_email]:
                sns_client.subscribe(
                    TopicArn=topic_arn,
                    Protocol='email',
                    Endpoint=email
                )

            # Publish the message
            sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject="Parcel Created: Details Inside"
            )
            messages.success(request, "Parcel created and notifications sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending notifications: {str(e)}")
            return redirect('create_parcel')

        return redirect('list_parcels')

    # Get transport records for dropdown
    transport_records = TransportRecord.objects.filter(user=request.user)
    return render(request, 'create_parcel.html', {'transport_records': transport_records})



# @login_required
# def create_parcel(request):
#     if request.method == 'POST':
#         sender_name = request.POST['sender_name']
#         sender_mobile = request.POST['sender_mobile']
#         sender_email = request.POST['sender_email']
#         receiver_name = request.POST['receiver_name']
#         receiver_mobile = request.POST['receiver_mobile']
#         receiver_email = request.POST['receiver_email']
#         origin = request.POST['origin']
#         destination = request.POST['destination']
#         weight = request.POST['weight']
#         transport_record_id = request.POST.get('transport_record')

#         # Fetch the transport record (if selected)
#         transport_record = None
#         if transport_record_id:
#             try:
#                 transport_record = TransportRecord.objects.get(id=transport_record_id, user=request.user)
#             except TransportRecord.DoesNotExist:
#                 messages.error(request, "Invalid transport record selected.")
#                 return redirect('create_parcel')

#         # Create the parcel
#         Parcel.objects.create(
#             user=request.user,  # Associate parcel with the logged-in user
#             sender_name=sender_name,
#             sender_mobile=sender_mobile,
#             sender_email=sender_email,
#             receiver_name=receiver_name,
#             receiver_mobile=receiver_mobile,
#             receiver_email=receiver_email,
#             origin=origin,
#             destination=destination,
#             weight=weight,
#             transport_record=transport_record,  # Link the transport record
#         )
#         messages.success(request, "Parcel created successfully!")
#         return redirect('list_parcels')

#     # Get transport records for dropdown
#     transport_records = TransportRecord.objects.filter(user=request.user)
#     return render(request, 'create_parcel.html', {'transport_records': transport_records})




### update parcel 
@login_required
def update_parcel(request, tracking_id):
    signup_link = f"{request.build_absolute_uri('/')}"
    parcel = get_object_or_404(Parcel, tracking_id=tracking_id, user=request.user)

    if request.method == 'POST':
        parcel.status = request.POST['status']
        transport_record_id = request.POST.get('transport_record')

        # Fetch the transport record (if selected)
        transport_record = None
        if transport_record_id:
            try:
                transport_record = TransportRecord.objects.get(id=transport_record_id, user=request.user)
            except TransportRecord.DoesNotExist:
                messages.error(request, "Invalid transport record selected.")
                return redirect('update_parcel', tracking_id=tracking_id)

        parcel.transport_record = transport_record  # Update the transport record
        parcel.save()

        # messages.success(request, "Parcel status and transport record updated successfully!")
        # return redirect('list_parcels')
    
        tracking_url = f"{signup_link}public/track/"
                # Prepare notification details
        message = f"""
        Parcel Details:


        Sender: {parcel.sender_name}
        Mobile: {parcel.sender_mobile}
        Email: {parcel.sender_email}

        Receiver: {parcel.receiver_name}
        Mobile: {parcel.receiver_mobile}
        Email: {parcel.receiver_email}

        Origin: {parcel.origin}
        Destination: {parcel.destination}

        Status: {parcel.status}

        Assigned Vehicle:
        Vehicle ID: {parcel.transport_record.vehicle_id if parcel.transport_record else 'Not Assigned'}
        Destination: {parcel.transport_record.destination if parcel.transport_record else 'Not Assigned'}
        Driver Name: {parcel.transport_record.driver_name if parcel.transport_record else 'Not Assigned'}
        Departure Date: {parcel.transport_record.departure_date.strftime('%b. %d, %Y') if parcel.transport_record else 'Not Assigned'}
        Arrival Date: {parcel.transport_record.arrival_date.strftime('%b. %d, %Y') if parcel.transport_record else 'Not Assigned'}

        ##################################################################

        Tracking ID: {parcel.tracking_id}
        To track the parcel, go to the following URL: {tracking_url}

        ##################################################################
        """

        # Publish the notification to SNS
        sns_client = boto3.client(
            'sns',
            region_name=settings.AWS_REGION,
            # aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            # aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            # aws_session_token=settings.AWS_SESSION_TOKEN
        )
        topic_arn = settings.AWS_SNS_TOPIC_ARN

        try:
            # Publish the message
            sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject="Parcel Status Update:"
            )
            messages.success(request, "Parcel Status Update and notifications sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending notifications: {str(e)}")
            return redirect('list_parcels')
        return redirect('list_parcels')
        


    # Get transport records for dropdown
    transport_records = TransportRecord.objects.filter(user=request.user)
    return render(request, 'update_parcel.html', {'parcel': parcel, 'transport_records': transport_records})




def public_track_parcel(request):
    tracking_id = request.GET.get('tracking_id')
    parcel = None

    if tracking_id:
        try:
            # Validate the tracking ID as a UUID
            uuid_obj = UUID(tracking_id, version=4)
            parcel = Parcel.objects.get(tracking_id=uuid_obj)
        except ValueError:
            messages.error(request, "Invalid Tracking ID format. Please enter a valid UUID.")
        except Parcel.DoesNotExist:
            messages.error(request, "No parcel found with the provided Tracking ID.")

    return render(request, 'public_track_parcel.html', {'parcel': parcel})
# def public_track_parcel(request):
#     tracking_id = request.GET.get('tracking_id')
#     parcel = None

#     if tracking_id:
#         try:
#             # Validate the tracking ID as a UUID
#             uuid_obj = UUID(tracking_id, version=4)
#             parcel = Parcel.objects.get(tracking_id=uuid_obj)
#         except ValueError:
#             messages.error(request, "Invalid Tracking ID format. Please enter a valid UUID.")
#         except Parcel.DoesNotExist:
#             messages.error(request, "No parcel found with the provided Tracking ID.")

#     return render(request, 'public_track_parcel.html', {'parcel': parcel})

def user_home(request):
    return render(request, 'user_home.html')
