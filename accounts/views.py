from django.shortcuts import render,redirect
from .forms import loginForms,regForms
from django.contrib.auth import authenticate
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
            email = regform.cleaned_data.get('email')

            
            if User_Details.objects.filter(email=email).exists():
                
                regform.add_error('email', 'Email already exists. Please choose another email.')

                return render(request, 'register.html', {'form': regform})
            
            request.session['user_data']={
                'first_name': regform.cleaned_data.get('first_name'),
                'last_name': regform.cleaned_data.get('last_name'),
                'phone': regform.cleaned_data.get('phone'),
                'email': email,
                'password': regform.cleaned_data.get('password'),
                'username': email
            }

            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['otp_created_at'] = timezone.now().isoformat()

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your OTP code is {otp}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=regform.cleaned_data.get('phone')
            )

            return redirect(otp_verification)

            
        
    else:
        regform = regForms()


    return render(request, 'accounts/registration.html', {'regform': regform})

def otp_verification(request):
    if request.method == 'POST':
        input_otp =request.POST.get('otp')
        otp = request.session.get('otp')
        otp_created_at =datetime.fromisoformat(request.session.get('otp_created_at'))
        
        time_diff = timezone.now() - otp_created_at

        if time_diff.total_seconds() <= 600:
            if input_otp == otp:
                user_data = request.session.get('user_data')

                if user_data:
                    User = get_user_model()
                    user = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone=user_data['phone'],
                    email=user_data['email'],
                    
                )
                user.set_password(user_data['password'])  
                user.save()

                del request.session['user_data']
                del request.session['otp']
                del request.session['otp_created_at']

                messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
            
            else:
                messages.success(request, "Oops!! Invalid otp,Try again.")
        else:
            messages.success(request, "Oops!! otp expired")                

   
         

    return render(request, 'accounts/otp.html' )

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        loginform = loginForms(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:            
            login(request, user)
            if user.is_staff:

                response = redirect('dashboard')            
                return response
            else:
                return redirect('home')
        else:
            loginform.add_error('username', "User doesn't exist.")

    else:
        loginform = loginForms()
    
    return render(request, 'accounts/login.html', {'loginform': loginform})


    



