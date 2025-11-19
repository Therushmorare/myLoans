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

def admin_page(request):
    return render(request, "admin/index.html")