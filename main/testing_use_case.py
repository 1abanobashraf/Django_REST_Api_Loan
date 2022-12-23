# %%
import requests

borrower_name = "Abanod"
investor_name = "Ashraf"
investor_balance = 5500.0
loan_amount = 5000.0
loan_period = 6
offer_interest_rate = 0.15
loan_amount_settled = 895.84

borrower_id = 0
investor_id = 0
loan_id = 0
offer_id = 0

# %%
res = requests.post("http://localhost:8000/create_borrower",
                    data={"name": borrower_name})
data = res.json()
borrower_id = int(data['id'])
print("Borrower have been successfully registered.")

# %%
res = requests.post("http://localhost:8000/create_investor",
                    data={"name": investor_name, "balance": investor_balance})
data = res.json()
investor_id = int(data['id'])
print("Investor have been successfully registered.")

# %%
res = requests.post("http://localhost:8000/loan_request",
                    data={"borrower": borrower_id, "amount": loan_amount, "period": loan_period})
data = res.json()
loan_id = int(data['id'])
print("Loan request has been successfully made.")

# %%
res = requests.post("http://localhost:8000/offer_request",
                    data={"borrower": borrower_id, "investor": investor_id, "loan": loan_id, "interest_rate": offer_interest_rate})
data = res.json()
offer_id = int(data['id'])
print("Offer to the borrower has been successfully submitted.")

# %%
res = requests.post("http://localhost:8000/accept_offer",
                    data={"id": offer_id})
data = res.json()
print(data['Message'])

# %%
# Schedular Simulator
for i in range(loan_period):
    res = requests.post("http://localhost:8000/monthly_payment",
                        data={"id": loan_id, "amount_settled": loan_amount_settled})
    data = res.json()
    print(data['Message'])
