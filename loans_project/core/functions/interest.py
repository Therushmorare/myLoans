from loans_project.models.loans import Loan
from loans_project.models.repayments import Repayment
from loans_project.models.interest import Interest
from loans_project.models.handover import Handover
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.timezone import now

#this will be used as a background job
def interest_checker_job(user_id):
    try:
        # safer to use client_id if it's a FK to User
        loans = Loan.objects.filter(user_id=user_id)

        for loan in loans:
            calculate_interest(loan.loan_id)  # or loan.id depending on your calc function

        return True
    except Exception as e:
        print(f"Could not calculate loan interest: {e}")
        return False

def calculate_interest(loan_id):
    try:
        loan = Loan.objects.filter(loan_id=loan_id).first()
        if not loan:
            return None

        # No money sent → no interest
        if not loan.disbursed_at:
            return None

        principal = Decimal(loan.amount)
        annual_rate = Decimal(loan.interest_rate) / Decimal(100)
        daily_rate = annual_rate / Decimal(365)

        # Interest record
        interest, created = Interest.objects.get_or_create(
            loan_id=loan.loan_id,
            user=loan.user,
            defaults={
                "incurred_amount": Decimal("0.00"),
                "last_calculated_at": loan.disbursed_at
            }
        )

        # HARD GUARD FOR OLD LOANS
        if interest.last_calculated_at < loan.disbursed_at:
            interest.last_calculated_at = loan.disbursed_at
            interest.incurred_amount = Decimal("0.00")
            interest.save()

        last_calc = interest.last_calculated_at
        today = now()

        if today <= last_calc:
            return interest

        days_elapsed = (today - last_calc).days
        if days_elapsed <= 0:
            return interest

        # Daily simple interest
        new_interest = principal * daily_rate * Decimal(days_elapsed)

        interest.incurred_amount += new_interest
        interest.last_calculated_at = today
        interest.save()

        # repayments
        repayments = Repayment.objects.filter(loan=loan)
        repaid_total = sum((r.amount for r in repayments), Decimal("0.00"))

        total_due = principal + interest.incurred_amount

        # due date from DISBURSEMENT
        due_date = loan.disbursed_at + timedelta(days=30 * loan.duration_months)

        if today > due_date and repaid_total < total_due:
            Handover.objects.get_or_create(
                loan=loan,
                user=loan.user,
                defaults={
                    "amount": total_due - repaid_total,
                    "status": "OPEN"
                }
            )

        return interest

    except Exception as e:
        print(f"Could not calculate interest: {e}")
        return None