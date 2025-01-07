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

            # Check if email or unique fields already exist
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
def Login_auth(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            email = request.POST['email']
            raw_password = request.POST['password']

            # Find user by email
            user = UserRegistration.objects.filter(email=email).first()
            if user is None:
                return HttpResponse("Invalid email or password.", status=401)

            # Check password
            if not check_password(raw_password, user.password):
                return HttpResponse("Invalid email or password.", status=401)

            # Set user role and redirect based on role
            if user.role == 'admin':
                return redirect('user_dashboard')  # Redirect to admin dashboard
            elif user.role == 'user':
                return redirect('user_dashboard')  # Redirect to user dashboard

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    return render(request, 'authenticate/login.html')