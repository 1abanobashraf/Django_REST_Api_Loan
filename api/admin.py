from django.contrib import admin

# Register your models here.

from .models import Borrower, Investor, Loan, Offer


class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class InvestorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'investor', 'status')
    list_filter = ('borrower', 'investor', 'status')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'investor', 'loan', 'status')
    list_filter = ('borrower', 'investor', 'status')


admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Offer, OfferAdmin)
