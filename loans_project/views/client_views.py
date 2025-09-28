from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from loans_project.models.client import Client
from loans_project.core.clients import auth
from loans_project.core.functions import loan_packages

# Dashboard
@login_required(login_url='/login/')  # Redirect to login if not signed in
def client_dashboard(request):
    return render(request, "clients/dashboard.html", {"user": request.user})

@login_required(login_url='/login/')
def loan_type(request):
    context = {
        "user": request.user,
        "packages": loan_packages
    }
    return render(request, "clients/loan_type.html", context=context)

@login_required(login_url='/login/')
def apply_for_loan(request, id):
    client = get_object_or_404(Client, id=id)

    if client:
        return client

    if request.method == "POST":
        user_id = id
        package_name = request.POST.get("package")
        term = request.POST.get("term")
        description = request.POST.get("description")
        interest = request.POST.get(interest)
        duration = request.POST.get(duration)

        context = {
        "user_id": user_id,
        "package_name": package_name,
        "term": term,
        "description": description,
        "interest": interest,
        "duration": duration
        }

        return render(request, "clients/apply.html", context=context)

@login_required(login_url='/login/')
def processApplication(request, id):
    client = get_object_or_404(Client, id=id)

    if client:
        return client
    
    if request.method == "POST":
        user_id = id
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        reason = request.POST.get("reason")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        citizen = request.POST.get("citizen")
        id_number = request.POST.get("ID_number")
        email = request.POST.get("email")
        phone = request.POST.get("phone_number")
        address = request.POST.get("address")   
        postal_code = request.POST.get("postal_code")
        city = request.POST.get("city")
        province = request.POST.get("province")
        company = request.POST.get("company")
        position = request.POST.get("position")
        salary = request.POST.get("salary")
        id_document = request.FILES["ID_file"]
        proof_of_income = request.FILES["proof_of_income"]
        proof_of_res = request.FILES["proof_of_res"]
        employment = request.FILES["employment_doc"]