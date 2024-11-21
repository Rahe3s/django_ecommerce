from django.shortcuts import render,redirect
from .forms import regForms,LoginForms
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User_Details
import random
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model




def registration(request):
    if request.method == 'POST':
        regform = regForms(request.POST)
        if regform.is_valid():
            phone = regform.cleaned_data.get('phone')
            
            if User_Details.objects.filter(phone=phone).exists():
                regform.add_error('phone', 'Phone number already exists. Please choose another phone number.')
                messages.error(request, 'Phone number already exists. Please choose another phone number.')
                return render(request, 'accounts/registration.html', {'regform': regform})

            # Store user data in session
            request.session['user_data'] = {
                'first_name': regform.cleaned_data.get('first_name'),
                'last_name': regform.cleaned_data.get('last_name'),
                'email': regform.cleaned_data.get('email'),
                'phone': phone,
                'password': regform.cleaned_data.get('password'),
                'username': phone
            }

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['otp_created_at'] = timezone.now().isoformat()

            try:
                # Send OTP via SMS
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Your OTP code is {otp}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone
                )

                messages.success(request, 'Verify! An OTP has been sent to your phone.')
                return redirect('otp_verification')

            except Exception as e:
                messages.error(request, f'Error sending OTP:')
                return render(request, 'accounts/registration.html', {'regform': regform})
        
    else:
        regform = regForms()

    return render(request, 'accounts/registration.html', {'regform': regform})



def otp_verification(request):
    try:
        if request.method == 'POST':
            input_otp = request.POST.get('otp')
            otp = request.session.get('otp')
            otp_created_at = datetime.fromisoformat(request.session.get('otp_created_at'))

            time_diff = timezone.now() - otp_created_at

            if time_diff.total_seconds() <= 120:  # Check the OTP time expired or not
                if input_otp == otp:
                    user_data = request.session.get('user_data')

                    if user_data:
                        # Save user to the database
                        User = get_user_model()
                        user = User(
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            phone=user_data['phone'],
                            email=user_data['email'],
                        )
                        user.set_password(user_data['password'])
                        user.save()

                        # clear session data
                        del request.session['user_data']
                        del request.session['otp']
                        del request.session['otp_created_at']

                        messages.success(request, "Registration successful. You can now log in.")
                        return redirect('login_page')
                else:
                    messages.error(request, "Oops!! Invalid OTP. Try again.")
            else:
                messages.error(request, "Oops!! OTP expired.")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred:")

    return render(request, 'accounts/otp_verification.html')

def login_page(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('home')

        if request.method == 'POST':
            loginform = LoginForms(request.POST)

            if loginform.is_valid():
                phone = loginform.cleaned_data.get('phone')
                password = loginform.cleaned_data.get('password')

                user = authenticate(request, phone=phone, password=password)

                if user is not None:
                    login(request, user)

                    messages.success(request, f"Welcome back, {user.first_name}!")

                    if user.is_staff:
                        return redirect('admin_dashboard')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, "Invalid phone number or password.")
            else:
                messages.error(request, "Please correct the highlighted errors.")
        else:
            loginform = LoginForms()

        return render(request, 'accounts/login.html', {'loginform': loginform})

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return render(request, 'accounts/login.html', {'loginform': LoginForms()})

def logout_page(request):
    try:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('login_page')
    
    except Exception as e:
        
        messages.error(request, f"An unexpected error occurred during logout: {str(e)}")
        return redirect('login_page')


    



