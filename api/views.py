from django.shortcuts import render

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import api.models as models
from django.shortcuts import render
from django.http import JsonResponse
from .models import Borrower, Investor, Loan, Offer
from .serializers import borrowerSerializer, investorSerializer, loanSerializer, offerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
def create_borrower(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        if "name" in data:
            borrower = models.Borrower(name=data["name"])
            borrower.save()
            # return JsonResponse({"Message": f"{borrower.name}, you have been successfully registered as a Borrower."})
            return JsonResponse({"id": borrower.id})

        else:
            return JsonResponse({"Message": "Missing the name field."})
    else:
        return JsonResponse({"Message": "Sorry not the expected HTTP Method."})


@csrf_exempt
def create_investor(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        if "name" and "balance" in data:
            investor = models.Investor(
                name=data["name"], balance=float(data["balance"]))
            investor.save()
            # return JsonResponse({"Message": f"{investor.name}, you have been successfully registered as an Investor with a sufficient balance of ${investor.balance}."})
            return JsonResponse({"id": investor.id})
        else:
            return JsonResponse({"Message": "Missing the name or balance field."})
    else:
        return JsonResponse({"Message": "Sorry not the expected HTTP Method."})


@csrf_exempt
def loan_request(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        if "borrower" and "amount" and "period" in data:
            bor = models.Borrower.objects.get(id=data['borrower'])
            loan = models.Loan(borrower=bor, amount=float(
                data['amount']), period=data['period'])
            loan.save()
            # return JsonResponse({"Message": "Your loan request has been successfully made."})
            return JsonResponse({"id": loan.id})

        else:
            return JsonResponse({"Message": "Missing one of the amount or period or borrower field."})
    else:
        return JsonResponse({"Message": "Sorry not the expected HTTP Method."})


@csrf_exempt
def offer_request(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        if "borrower" and "investor" and "loan" and "interest_rate" in data:
            bor = models.Borrower.objects.get(id=data['borrower'])
            inv = models.Investor.objects.get(id=data['investor'])
            loan = models.Loan.objects.get(id=data['loan'])
            offer = models.Offer(borrower=bor, investor=inv, loan=loan,
                                 interest_rate=float(data['interest_rate']))
            offer.save()
            # return JsonResponse({"Message": "Your offer to the borrower has been successfully submitted."})
            return JsonResponse({"id": offer.id})
        else:
            return JsonResponse({"Message": "Missing one of the borrower or investor or loan interest_rate field."})
    else:
        return JsonResponse({"Message": "Sorry not the expected HTTP Method."})


@csrf_exempt
def accept_offer(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        if "id" in data:
            req = models.Offer.objects.get(id=data['id'])
            req.status = "Accepted"
            req.save()
            total_loan_amount = req.loan.amount + 3.00
            if (req.investor.balance >= total_loan_amount):
                loan = models.Loan.objects.get(id=int(req.loan.id))
                loan.investor = req.investor
                loan.interest_rate = req.interest_rate
                loan.status = "Funded"
                loan.save()
                principal_amount = loan.amount
                interest_amount = (
                    principal_amount*loan.interest_rate)/(12/loan.period)
                final_amount_per_month = (
                    principal_amount + interest_amount) / loan.period
                return JsonResponse({"Message": f"The proposed offer has been accepted and the loan will be funded successfully. You will be paying ${final_amount_per_month} every month for {loan.period} Month(s)."})
            else:
                return JsonResponse({"Message": "The proposed offer has been accepted, but unfortunately the loan will not be funded due to the investor insufficient balance."})
        else:
            return JsonResponse({"Message": "Missing the id field."})
    else:
        return JsonResponse({"Message": "Sorry not the expected HTTP Method."})


@csrf_exempt
def monthly_payment(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        if "id" and "amount_settled" in data:
            loan = models.Loan.objects.get(id=data['id'])
            loan.amount_settled = loan.amount_settled + \
                float(data['amount_settled'])

            principal_amount = loan.amount
            interest_amount = (
                principal_amount*loan.interest_rate)/(12/loan.period)
            final_amount = (principal_amount + interest_amount)

            if (loan.amount_settled >= final_amount):
                loan.status = "Completed"
                loan.save()
                return JsonResponse({"Message": "Congratulations! All the payments are successfully paid back to the investor."})
            else:
                loan.save()
                return JsonResponse({"Message": "See you next month."})

        else:
            return JsonResponse({"Message": "Missing one of the id or amount_settled field."})
    else:
        return JsonResponse({"Message": "Sorry not the expected HTTP Method."})


# get/post in (borrower,investor,loan,offer)

@api_view(['GET', 'POST'])
def borrower_list(request, format=None):

    if request.method == 'GET':
        borrowers = Borrower.objects.all()
        serializer = borrowerSerializer(borrowers, many=True)
        return JsonResponse({"Borrowers": serializer.data})

    if request.method == 'POST':
        serializer = borrowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def investor_list(request, format=None):

    if request.method == 'GET':
        investor = Investor.objects.all()
        serializer = investorSerializer(investor, many=True)
        return JsonResponse({"Investors": serializer.data})

    if request.method == 'POST':
        serializer = investorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def loan_list(request, format=None):

    if request.method == 'GET':
        loan = Loan.objects.all()
        serializer = loanSerializer(loan, many=True)
        return JsonResponse({"Loans": serializer.data})

    if request.method == 'POST':
        serializer = loanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def offer_list(request, format=None):

    if request.method == 'GET':
        offer = Offer.objects.all()
        serializer = offerSerializer(offer, many=True)
        return JsonResponse({"Offers": serializer.data})

    if request.method == 'POST':
        serializer = Offer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# get/put/delete in (borrower,investor,loan,offer)

@api_view(['GET', 'PUT', 'DELETE'])
def borrower_detail(request, id, format=None):
    try:
        borrower = Borrower.objects.get(pk=id)
    except Borrower.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = borrowerSerializer(borrower)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = borrowerSerializer(borrower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        borrower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def investor_detail(request, id, format=None):

    try:
        investor = Investor.objects.get(pk=id)
    except Investor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = investorSerializer(investor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = investorSerializer(investor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        investor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def loan_detail(request, id, format=None):

    try:
        loan = Loan.objects.get(pk=id)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = loanSerializer(loan)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = loanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def offer_detail(request, id, format=None):

    try:
        offer = Offer.objects.get(pk=id)
    except Offer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = offerSerializer(offer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = offerSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
