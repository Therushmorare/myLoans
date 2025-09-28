from decimal import Decimal
from models.loans import Loan
from functions.application_filters import filter_loan_application
import uuid

def process_loan_application(
    user,
    package, loan_term, interest, duration, amount, date, reason,
    first_name, last_name, citizen, id_number, email, phone,
    address, postal_code, city, province, company, position, 
    salary, id_document, proof_of_income, proof_of_res, employment
):
    """
    Process a loan application:
    - Check eligibility via filter_loan_application
    - Save Loan with status APPROVED or REJECTED
    """
    try:
        # Check application eligibility
        application_status = filter_loan_application(duration, amount, interest, citizen, salary)

        # Generate unique loan_id
        loan_id = str(uuid.uuid4())[:8].upper()  # short unique ref

        # Create Loan record
        loan = Loan.objects.create(
            user=user,
            loan_id=loan_id,
            package=package,
            loan_term=loan_term,
            interest_rate=Decimal(interest),
            duration_months=int(duration),
            amount=Decimal(amount),
            applied_at=date,
            status="APPROVED" if application_status != "REJECT" else "REJECTED",
            reason=reason,
            first_name=first_name,
            last_name=last_name,
            citizen=bool(citizen),
            id_number=id_number,
            email=email,
            phone=phone,
            address=address,
            postal_code=postal_code,
            city=city,
            province=province,
            company=company,
            position=position,
            salary=Decimal(salary) if salary else None,
            id_document=id_document,
            proof_of_income=proof_of_income,
            proof_of_residence=proof_of_res,
            employment_doc=employment
        )

        return loan

    except Exception as e:
        print(f"Error processing loan application: {e}")
        return None