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
            dti_message = "Excellent DTI ratio"
        elif 30 < dti_value <= 40:
            dti_score = 75
            dti_message = "Moderate DTI ratio"
        else:
            dti_score = 25
            dti_message = "High DTI ratio — considered risky"
        total_score += dti_score

        # Step 4: Decision
        if total_score >= 150:
            decision = "passed automatic evaluation"
            status_code = 200
            recommendation = "Your loan application is likely to proceed to the next stage."
        else:
            decision = "failed automatic evaluation"
            status_code = 400
            recommendation = "Consider reducing your DTI or increasing your monthly income before reapplying."

        # Step 5: Build detailed response
        response = {
            "loan_amount": f"{amount:.2f}",
            "loan_duration_months": duration_in_months,
            "annual_interest_rate": f"{annual_interest:.2f}%",
            "estimated_monthly_emi": f"{emi_value:.2f}",
            "monthly_salary": f"{monthly_salary:.2f}",
            "dti_percentage": f"{dti_value:.2f}%",
            "dti_score": dti_score,
            "dti_message": dti_message,
            "total_score": total_score,
            "decision": decision,
            "recommendation": recommendation
        }

        return response, status_code

    except Exception as e:
        print(f"Could not create application score: {e}")
        return {"message": "An error occurred while evaluating your application"}, 500