from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from loans_project.models.client import Client
from loans_project.models.loans import Loan
from loans_project.models.interest import Interest
from loans_project.models.repayments import Repayment
from loans_project.core.clients import auth, loan_apply
from loans_project.core.functions.finance_packages import loan_packages
from loans_project.core.functions import interest
from django.db.models import Sum
import django_rq #Replace with celery on big apps

#landing page
def landing_page(request):
    context = {
        "packages": loan_packages
    }
    return render(request, "landing_page.html", context=context)

# Dashboard
@login_required(login_url='/login/')
def client_dashboard(request):
    # enqueue background job
    queue = django_rq.get_queue("default")
    queue.enqueue(interest.interest_checker_job, request.user.id)

    # calculate stats
    total_loans = Loan.objects.filter(user=request.user, status='APPROVED') \
                              .aggregate(total=Sum('amount'))['total'] or 0

    total_paid = Repayment.objects.filter(user=request.user, status='SUCCESS') \
                                  .aggregate(total=Sum('amount'))['total'] or 0

    total_owing = total_loans - total_paid

    interest_payable = Interest.objects.filter(user=request.user) \
                                       .aggregate(total=Sum('incurred_amount'))['total'] or 0

    context = {
        'user': request.user,
        'total_loans': total_loans,
        'total_paid': total_paid,
        'total_owing': total_owing,
        'interest_to_pay': interest_payable
    }

    return render(request, "clients/dashboard.html", context=context)

# My loan applications
@login_required(login_url='/login/')
def loan_applications(request):
    loans = Loan.objects.filter(user=request.user)  # filter by user object
    user = request.user  # already the logged-in user
    context = {
        "user": user,
        "loans": loans
    }
    return render(request, "clients/applications.html", context)

# My account details
@login_required(login_url='/login/')
def account(request):
    user = request.user
    context = {
        "user": user
    }
    return render(request, "clients/account.html", context)

# My portfolio
@login_required(login_url='/login/')
def portfolio(request):
    loans = Loan.objects.filter(user=request.user)
    interests = Interest.objects.filter(user=request.user)
    repayments = Repayment.objects.filter(user=request.user)
    total_loans = Loan.objects.filter(user=request.user, status='APPROVED') \
                              .aggregate(total=Sum('amount'))['total'] or 0

    total_paid = Repayment.objects.filter(user=request.user, status='SUCCESS') \
                                  .aggregate(total=Sum('amount'))['total'] or 0

    total_owing = total_loans - total_paid

    interest_payable = Interest.objects.filter(user=request.user) \
                                       .aggregate(total=Sum('incurred_amount'))['total'] or 0

    context = {
        "user": request.user,
        "loans": loans,
        "interests": interests,
        "repayments": repayments,
        "total_loans": total_loans,
        "total_paid": total_paid,
        "total_owing": total_owing,
        "interest_to_pay": interest_payable

    }
    return render(request, "clients/portfolio.html", context)

#Repayments
@login_required(login_url='/login/')
def payments(request):
    loans = Loan.objects.filter(user=request.user)
    interests = Interest.objects.filter(user=request.user)
    repayments = Repayment.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'loans': loans,
        'interests': interests,
        'payements': repayments,
    }
    return render(request, "clients/repayments.html", context=context)

#start loan application
@login_required(login_url='/login/')
def loan_type(request):
    context = {
        "user": request.user,
        "packages": loan_packages
    }
    return render(request, "clients/loan_type.html", context=context)

@login_required(login_url='/login/')
def apply_for_loan(request):

    if request.method == "POST":
        user_id = request.user.id
        package_name = request.POST.get("package")
        term = request.POST.get("term")
        description = request.POST.get("description")
        interest = request.POST.get("interest")
        duration = request.POST.get("duration")

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
            return redirect("apply")

    # if GET request, maybe render the application form
    return render(request, "clients/apply.html", {"client": client})

@login_required(login_url='/login/')
def submit_payment(request, loan_id):
    # Fetch the loan for the logged-in user
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)

    # Calculate total interest incurred
    loan_interest = Interest.objects.filter(loan=loan).aggregate(total=Sum('incurred_amount'))['total'] or 0

    # Calculate total already repaid (only SUCCESS payments)
    loan_repaid = Repayment.objects.filter(loan=loan, status="SUCCESS").aggregate(total=Sum('amount'))['total'] or 0

    # Max payable
    max_payable = loan.amount + loan_interest - loan_repaid

    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        payment_type = request.POST.get("payment_type")

        if amount > max_payable:
            messages.error(request, f"Amount exceeds maximum payable: {max_payable}")
            return redirect('dashboard')  # or back to loan page

        # Create a new repayment (status could be "PENDING" if using a payment gateway)
        Repayment.objects.create(
            loan=loan,
            amount=amount,
            status="PENDING",  # or "SUCCESS" if confirmed
            reference=None  # payment gateway ref
        )

        messages.success(request, f"Payment of {amount} submitted for {payment_type}.")
        return redirect('dashboard')

    return redirect('dashboard')