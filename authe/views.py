from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from .models import UserRegistration
from django.contrib.auth.hashers import check_password

@transaction.atomic
def Register_auth(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        try:
            # Extract data from the form
            first_name = request.POST['username']
            email = request.POST['email']
            date_of_birth = request.POST['DOB']
            aadhar = request.POST['aadhar']
            pancard = request.POST['pancard']
            raw_password = request.POST['password']
            address = request.POST['address']
            role = request.POST.get('role', 'user')  # Default role is 'user'

            if UserRegistration.objects.filter(email=email).exists():
                return HttpResponse("Email is already registered.", status=400)
            if UserRegistration.objects.filter(aadhar=aadhar).exists():
                return HttpResponse("Aadhar card is already registered.", status=400)
            if UserRegistration.objects.filter(pancard=pancard).exists():
                return HttpResponse("PAN card is already registered.", status=400)

            # Create the user and hash the password
            user = UserRegistration(
                first_name=first_name,
                email=email,
                date_of_birth=date_of_birth,
                aadhar=aadhar,
                pancard=pancard,
                address=address,
                role=role,
            )
            user.set_password(raw_password)  # Hash the password
            user.save()

            return redirect('login')  # Redirect to login page
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return render(request, 'authenticate/register.html')
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from .models import UserRegistration
from django.utils.timezone import now

def Login_auth(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            raw_password = request.POST.get('password')
            
            # Check if the user exists
            user = UserRegistration.objects.filter(email=email).first()
            if user is None or not check_password(raw_password, user.password):
                return HttpResponse("Invalid email or password.", status=401)
            
            # Update the last login time
            user.last_login = now()
            user.save()

            # Set the backend explicitly
            user.backend = 'authe.auth_backends.UserRegistrationBackend'

            # Log the user in (establish session)
            login(request, user)

            # Redirect based on user role
            if user.role == 'admin':
                return redirect('add_stocks')  # Replace with the correct URL name for admin dashboard
            elif user.role == 'user':
                return redirect('user_dashboard')  # Replace with the correct URL name for user dashboard

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return render(request, 'authenticate/login.html')
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required
def logout_view(request):
    """
    Custom view to handle user logout.
    """
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')
