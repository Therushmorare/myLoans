from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from loans_project.models.client import Client
from loans_project.core.clients import auth

#login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)  # use email
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, "clients/login.html")

# signup
def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "clients/signup.html")

        if Client.objects.filter(email=email).exists():
            messages.error(request, "User with that email already exists!")
            return render(request, "clients/signup.html")

        try:
            user = Client.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                password=password
            )
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")

        except Exception as e:
            print(f"Signup Error: {e}")
            messages.error(request, "Something went wrong, please try again later!")

    return render(request, "clients/signup.html")

#forgot password
def forgot_pass_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        result = auth.user_forgot_password(request, email)
        if result:
            return result
    
    return render(request, "clients/forgot.html")

#logout
def logout_view(request):
    logout(request)
    return redirect("login")