from rest_framework import serializers
from .models import Borrower, Investor, Loan, Offer


class borrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'name']


class investorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['id', 'name', 'balance']


class loanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'borrower', 'investor', 'amount',
                  'period', 'interest_rate', 'status', 'amount_settled']
        depth = 1


class offerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'borrower', 'investor',
                  'loan', 'interest_rate', 'status']
        depth = 1
