from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from models.client import Client
from core.clients import auth

def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        result = auth.user_signup(request, first_name, last_name, email, phone_number, password, confirm_password)
        if result:
            return result

    return render(request, "clients/signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        result = auth.user_login(request, username, password)
        if result:
            return result

    return render(request, "clients/login.html")

def forgot_pass_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        result = auth.user_forgot_password(request, email)
        if result:
            return result
    
    return render(request, "clients/forgot.html")

def logout_view(request):
    logout(request)
    return redirect("login")