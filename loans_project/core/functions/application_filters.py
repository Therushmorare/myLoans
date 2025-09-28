from loans_project.core.functions.calculate_monthly_repayment import *

def filter_loan_application(duration_in_months, amount, annual_interest, citizen, monthly_salary):
    try:
        # Step 1: Calculate EMI and DTI
        emi_value = monthly_repayment(amount, annual_interest, duration_in_months)
        dti_value = calculate_dti(emi_value, monthly_salary)

        total_score = 0

        # Step 2: Citizenship check
        if citizen.lower() == "yes":
            citizen_score = 100
        else:
            citizen_score = 50
        total_score += citizen_score

        # Step 3: DTI scoring
        if dti_value <= 30:
            dti_score = 100
        elif 30 < dti_value <= 40:
            dti_score = 75
        else:
            dti_score = 25  # very risky
        total_score += dti_score

        # Step 4: Decision
        if total_score >= 150:
            return "ACCEPT"
        else:
            return "REJECT"
    
    except Exception as e:
        print(f"Could not create application score: {e}")
        return "NONE"