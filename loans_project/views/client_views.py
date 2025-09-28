from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from loans_project.models.client import Client
from core.clients import auth, loan_apply
from core.functions import loan_packages

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

    if request.method == "POST":
        # form fields
        package = request.POST.get("package_name")
        loan_term = request.POST.get("term")
        interest = request.POST.get("interest")
        duration = request.POST.get("duration")
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

        # file uploads
        id_document = request.FILES.get("ID_file")
        proof_of_income = request.FILES.get("proof_of_income")
        proof_of_res = request.FILES.get("proof_of_res")
        employment = request.FILES.get("employment_doc")

        # process loan
        loan = loan_apply.process_loan_application(
            user=request.user,
            package=package,
            loan_term=loan_term,
            interest=interest,
            duration=duration,
            amount=amount,
            date=date,
            reason=reason,
            first_name=first_name,
            last_name=last_name,
            citizen=citizen,
            id_number=id_number,
            email=email,
            phone=phone,
            address=address,
            postal_code=postal_code,
            city=city,
            province=province,
            company=company,
            position=position,
            salary=salary,
            id_document=id_document,
            proof_of_income=proof_of_income,
            proof_of_res=proof_of_res,
            employment=employment
        )

        if loan:
            messages.success(request, f"Loan {loan.loan_id} processed with status {loan.status}")
            return redirect("dashboard")
        else:
            messages.error(request, "Failed to process loan.")
            return redirect("apply_loan")

    # if GET request, maybe render the application form
    return render(request, "clients/apply_loan.html", {"client": client})
