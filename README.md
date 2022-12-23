# DJANGO-api (loan Use case)
This is a  Django REST project api for loan Use case (testing_use_case.py)

1- The borrower submits a loan request for $5,000 `loan amount` and 6 months `loan period`
2- The investor will submit an offer to the borrower with 15% `Annual Interest Rate`
3- The borrower will accept the offer
4- Checking if the investor has sufficient balance in their account to fund the `Total Loan Amount` (Loan Amount + Lenme Fee)
5- The loan will be funded successfully and the loan status will be `Funded`
6- Six monthly payments will be scheduled from the day the loan was funded successfully
7- Once all the payments are successfully paid back to the investor, the loan status will be changed to `Completed`
