from models.client import Client
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from functions.email_senders import forgot_pass_email

#login
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard", id=user.id)  # pass the user ID
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, "clients/login.html")

#sign up
def user_signup(request, first_name, last_name, email, phone_number, password, confirm_password):
      try:
            if password != confirm_password:
                  messages.error(request, "Passwords do not match!")
                  return render(request, "clients/signup.html")
            
            if Client.objects.filter(email=email).exists():
                  messages.error(request, "User with that email already exists!")
                  return render(request, "clients/signup.html")
            
            user = Client.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
            if user:
                messages.success(request, "Account created successfully! Please login.")
                return redirect("login")

      except Exception as e:
            print(f"Signup Error:{e}")
            messages.error(request, 'Something went wrong, please try again later!')
            return render(request, "clients/signup.html")
      
#forgot password
def user_forgot_password(request, email):
        try:
                if not email:
                        messages.error(request, "Please provide passsword")
                        return render(request, "clients/forgot.html")
                
                user = Client.objects.filter(email=email).first()

                if not user:
                        messages.error(request, "User with that email does not exist")
                        return render(request, "clients/forgot.html")
                
                try:
                        forgot_pass_email('Forgot Password', user.first_name, user.email, user.password)
                        messages.success(request, "An email was sent to your account, please view it for further assistence")
                        return render(request, "clients/forgot.html")
                except Exception as e:
                        print(f"Email Error:{e}")
                        messages.error(request, "Something went wrong when sending email")
                        return render(request, "clients/forgo.html")
        except Exception as e:
               print(f"Forgot Password Error:{e}")
               messages.error(request, 'Something went wrong, please try again later')
               return render(request, "clients/forgot.html")