from decimal import Decimal
from loans_project.models.loans import Loan
from loans_project.core.functions.application_filters import filter_loan_application
import uuid

def test_application_status(user, package, loan_term, interest, duration, amount, date, reason, first_name, last_name, citizen, id_number, email, phone, address, postal_code, city, province, company, position, salary, id_document, proof_of_income, proof_of_res, employment):
    try:
        # Check application eligibility
        application_status = filter_loan_application(duration, amount, interest, citizen, salary)
        return {
            'user': user,
            'package': package,
            'loan_term': loan_term,
            'interest': interest,
            'duration': duration,
            'amount': amount,
            'date': date,
            'reason': reason,
            'first_name': first_name,
            'last_name': last_name,
            'citizen': citizen,
            'id_number': id_number,
            'email': email,
            'phone': phone,
            'address': address,
            'postal_code': postal_code,
            'city': city,
            'province': province,
            'company': company,
            'position': position,
            'id_document': id_document,
            'proof_of_income': proof_of_income,
            'proof_of_res': proof_of_res,
            'employment': employment,
            'application_status': application_status,
            'duration': duration,
        }, 200
    
    except Exception as e:
        print(f"Loan test error:{e}")
        return {'message': 'Something went wrong'}, 500

#use the values received from test_application
def process_loan_application(user, package, loan_term, interest, duration, amount, date, reason, first_name, last_name, citizen, id_number, email, phone, address, postal_code, city, province, company, position, salary, id_document, proof_of_income, proof_of_res, employment):
    """
    Process a loan application:
    - Check eligibility via filter_loan_application
    - Save Loan with status APPROVED or REJECTED
    """
    try:

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
            status="PENDING",
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