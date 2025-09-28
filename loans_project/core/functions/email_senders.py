from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import threading
from datetime import datetime

#forgot password email
def forgot_pass_email(subject, name, email, password):
    try:
        # Render HTML template
        html_content = render_to_string(
            "email_templates/forgot_password.html",
            {"user_name": name, "password": password, "current_year": datetime.now().year}
        )
        # Plain text fallback
        text_content = f"Hello {name}, we noticed you forgot your password. Password: {password}!"

        # Create email
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,  # use your default sender
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")

        # Send asynchronously to avoid blocking
        threading.Thread(target=email_message.send).start()

    except Exception as e:
        print(f"Forgot Password Error: {e}")
