"""
URL configuration for loans_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from loans_project.views.auth_view import signup_view, login_view, logout_view, forgot_pass_view
from loans_project.views.client_views import *
from loans_project.views.admin_view import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', landing_page, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot/', forgot_pass_view, name='forgot'),

    # Use UUID converter for user/client IDs
    path('dashboard/', client_dashboard, name='dashboard'),
    path('select-loan-type/', loan_type, name='selectLoanType'),
    path('apply/', apply_for_loan, name='apply'),
    path('process-application/<uuid:id>', processApplication, name='processApplication'),
    path('my-loans/', loan_applications, name='loan_applications'),
    path('my-account/', account, name='account'),
    path('my-portfolio/', portfolio, name='portfolio'),
    path('my-payments/', payments, name='payments'),
    path('submit-payment/<uuid:loan_id>/', submit_payment, name='submit_payment'),
    path('admin-dashboard/', admin_page, name='admin_dashboard'),
    path('applications/', admin_applications, name='admin_applications'),
    path('django-rq/', include('django_rq.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)