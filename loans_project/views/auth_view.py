from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from loans_project.models.client import Client
from loans_project.models.admin import AdminUser
from loans_project.models.service_provider import ServiceProvider
from loans_project.core.clients import auth
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from loans_project.core.mfa import mfa_code_generation, mfa_email, verify_mfa_code


#login
def login_view(request):
    context = {}

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate across all users
        user = authenticate(request, email=email, password=password)

        if not user:
            context["error"] = "Invalid credentials"
            return render(request, "clients/login.html", context)

        if getattr(user, "status", None) in ["BANNED", "SUSPENDED"]:
            context["error"] = "Account is restricted"
            return render(request, "clients/login.html", context)

        # Store role in session for MFA redirect
        role = getattr(user, "role", None)
        request.session["mfa_user_id"] = str(user.id)
        request.session["mfa_role"] = role

        # Generate and send MFA code
        code = mfa_code_generation.save_mfa_code(user_id=user.id, user_type=role)
        mfa_email.send_mfa_email(email, role, code)

        return redirect("mfa_page")

    return render(request, "clients/login.html", context)

# signup
def signup_view(request):
    context = {}

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone_number = request.POST.get("phone_number", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Basic validation
        if not all([first_name, last_name, email, phone_number, password, confirm_password]):
            context["error"] = "All fields are required"
            return render(request, "clients/signup.html", context)

        if password != confirm_password:
            context["error"] = "Passwords do not match"
            return render(request, "clients/signup.html", context)

        # Password strength validation (IMPORTANT)
        try:
            validate_password(password)
        except ValidationError as e:
            context["error"] = e.messages[0]
            return render(request, "clients/signup.html", context)

        if Client.objects.filter(email=email).exists():
            context["error"] = "User with that email already exists"
            return render(request, "clients/signup.html", context)

        try:
            with transaction.atomic():
                user = Client.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    password=password,
                    role="CLIENT",
                    status="ACTIVE"
                )

            context["success"] = "Account created successfully. Please log in."
            return redirect("login")

        except Exception as e:
            print(f"Signup Error: {e}")
            context["error"] = "Something went wrong. Please try again."

    return render(request, "clients/signup.html", context)

#mfa
def mfa_view(request):
    context = {}

    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("mfa_user_id")
        role = request.session.get("mfa_role")

        if not user_id or not role:
            context["error"] = "Session expired. Please login again."
            return render(request, "clients/login.html", context)

        # Get user instance by role
        if role.upper() == "ADMIN":
            user = AdminUser.objects.filter(id=user_id).first()
        elif role.upper() == "PROVIDER":
            user = ServiceProvider.objects.filter(id=user_id).first()
        else:
            user = Client.objects.filter(id=user_id).first()

        if not user:
            context["error"] = "User not found"
            return render(request, "clients/login.html", context)

        # Verify MFA code
        is_verified, message = verify_mfa_code(user.id, code)
        if not is_verified:
            context["error"] = message
            return render(request, "clients/mfa.html", context)

        # MFA verified → log in user and redirect by role
        login(request, user)

        if role.upper() == "ADMIN":
            return redirect("admin_dashboard")
        elif role.upper() == "PROVIDER":
            return redirect("provider_dashboard")
        else:
            return redirect("client_dashboard")

    return render(request, "clients/mfa.html", context)

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