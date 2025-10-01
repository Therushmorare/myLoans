from django import template

register = template.Library()

@register.filter
def filterattr(items, args):
    """
    Filter a list of objects by attribute and value
    Usage: {{ items|filterattr:"attr,value" }}
    """
    try:
        attr, value = args.split(',')
        return [item for item in items if str(getattr(item, attr, '')) == value]
    except Exception:
        return []

@register.filter
def sum(objects, attr_name):
    try:
        return sum(getattr(obj, attr_name, 0) for obj in objects)
    except Exception:
        return 0

@register.filter
def get_interest(interests, loan_id):
    """
    Given a list of interest objects and a loan id,
    return the interest incurred for that loan or 0 if not found.
    """
    try:
        for interest in interests:
            if interest.loan_id == loan_id:
                return interest.incurred_amount
        return 0
    except Exception:
        return 0
    
@register.filter
def get_repaid(payments, loan_id):
    """
    Filters payments and sums amounts for a specific loan_id.
    """
    try:
        total_repaid = sum(payment.amount for payment in payments if payment.loan_id == loan_id)
        return total_repaid
    except Exception:
        return 0
    
@register.filter
def calculate_outstanding(loan, args):
    interest = args.get("interest")
    repaid = args.get("repaid")
    return loan.amount + interest.amount - repaid.total
