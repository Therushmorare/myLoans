from models.loans import Loan
from models.repayments import Repayment
from models.interest import Interest
from models.handover import Handover
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.timezone import now

#this will be used as a background job

def calculate_interest(loan_id):
    try:
        loan = Loan.objects.filter(loan_id=loan_id).first()
        if not loan:
            return None
        
        # convert stored values
        principal = Decimal(loan.amount)
        rate = Decimal(loan.loan_interest) / Decimal(100) 
        duration_months = int(loan.loan_duration)

        # check existing interest record
        interest, created = Interest.objects.get_or_create(
            loan_id=loan.loan_id,
            user=loan.user,
            defaults={"incurred_amount": Decimal(0)}
        )

        # compound interest (monthly compounding assumed)
        t = duration_months / 12
        total_interest = principal * ((1 + rate / 12) ** (12 * t) - 1)

        # update incurred interest
        interest.incurred_amount = total_interest
        interest.save()

        # total repayments
        repayments = Repayment.objects.filter(loan=loan)
        repaid_total = sum([r.amount for r in repayments], Decimal(0))

        # check due date (applied_at + duration)
        due_date = loan.applied_at + timedelta(days=30 * duration_months)
        if now() > due_date and repaid_total < (principal + total_interest):
            # escalate to handover
            Handover.objects.get_or_create(
                loan=loan,
                user=loan.user,
                defaults={
                    "amount": (principal + total_interest) - repaid_total,
                    "status": "OPEN"
                }
            )

        return interest

    except Exception as e:
        print(f"Could not check for interest: {e}")
        return None