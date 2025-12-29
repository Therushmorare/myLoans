from loans_project.utils.mail import send_mail

"""
Email template parsers
"""

#send account verification
def send_verification_email(email, verification_code):
    return send_mail(
        subject="Verification",
        template="email_templates/code_verification.html",
        context={
            "user_name": email,
            "keyToken": verification_code
        },
        recipients=[email]
    )

#send user credentials mail
def send_credentials_email(email, password):
    return send_mail(
        subject="Account Credentials",
        template="email_templates/credentials.html",
        context={
            "user_name": email,
            "password": password
        },
        recipients=[email]
    )

#generic email sender
def send_email(email, title, message):
    return send_mail(
        subject="Application Status",
        template="email_templates/alert.html",
        context={
            "user_name": email,
            "title": title,
            "message": message
        },
        recipients=[email]
    )

#comprehensive credentials
def send_credentials(email, employee_number, first_name, last_name, password):
    return send_mail(
        subject="Account Credentials",
        template="email_templates/credentials.html",
        context={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "acc_number": employee_number,
            "password": password
        },
        recipients=[email]
    )
