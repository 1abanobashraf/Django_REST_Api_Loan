from django.db import models
from pydata_google_auth import default

# Create your models here.


class Borrower(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"Name: {self.name} \n" \



class Investor(models.Model):
    name = models.CharField(max_length=100, blank=False)
    balance = models.FloatField(blank=False, default=0.0)

    def __str__(self):
        return f"Name: {self.name} \n" \
               f"Balance: {self.balance}"


class Loan(models.Model):
    Options = [("Pending", "Pending"), ("Funded", "Funded"),
               ('Completed', 'Completed')]

    borrower = models.ForeignKey(
        Borrower, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    amount = models.FloatField(blank=False, default=0.0)
    period = models.IntegerField(blank=False, default=0)
    interest_rate = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Options, default="Pending")
    amount_settled = models.FloatField(default=0.0)

    def __str__(self):
        return f"Borrower: {self.borrower} \n" \
               f"Investor: {self.investor} \n" \
               f"Loan Amount: {self.amount} \n" \
               f"Interest Rate: {self.interest_rate} \n" \
               f"Period: {self.period} Month(s) \n" \
               f"Status: {self.status} \n" \
               f"Setteled Amount: {self.amount_settled}"


class Offer(models.Model):
    Options = [("Pending", "Pending"), ('Accepted', 'Accepted')]

    borrower = models.ForeignKey(
        Borrower, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    interest_rate = models.FloatField(blank=False, default=0.0)
    status = models.CharField(
        max_length=20, choices=Options, default="Pending")

    def __str__(self):
        return f"Borrower: {self.borrower} \n" \
               f"Investor: {self.investor} \n" \
               f"Loan: {self.loan} \n" \
               f"Interest Rate: {self.interest_rate} \n" \
               f"Status: {self.status}"
