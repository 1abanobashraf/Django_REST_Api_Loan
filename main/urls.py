"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
import api.views as rest
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('create_borrower', rest.create_borrower),
    path('create_investor', rest.create_investor),
    path('loan_request', rest.loan_request),
    path('offer_request', rest.offer_request),
    path('accept_offer', rest.accept_offer),
    path('monthly_payment', rest.monthly_payment),

    path('borrower', rest.borrower_list),
    path('investor', rest.investor_list),
    path('loan', rest.loan_list),
    path('offer', rest.offer_list),

    path('borrower/<int:id>', rest.borrower_detail),
    path('investor/<int:id>', rest.investor_detail),
    path('loan/<int:id>', rest.loan_detail),
    path('offer/<int:id>', rest.offer_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
