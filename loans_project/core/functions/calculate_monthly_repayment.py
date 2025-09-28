#calculate monthly repayment

def monthly_repayment(principal_amount, annual_interest_rate, duration_in_months):
    try:
        monthly_rate = annual_interest_rate / 12  # e.g., 0.12 / 12
        numerator = principal_amount * monthly_rate * (1 + monthly_rate) ** duration_in_months
        denominator = (1 + monthly_rate) ** duration_in_months - 1

        emi = numerator / denominator
        return emi
    except Exception as e:
        print(f"Could not calculate monthly installments: {e}")
        return 0


def calculate_dti(emi, monthly_salary):
    try:
        dti = (emi / monthly_salary) * 100
        return dti
    except Exception as e:
        print(f"Could not calculate dti: {e}")
        return 0