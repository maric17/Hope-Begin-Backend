from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_approval_email(user_id, temp_password):
    try:
        user = User.objects.get(id=user_id)
        login_url = f"{settings.FRONTEND_URL}/login/carrier"
        
        subject = "Welcome to Hope Begins - Your Application is Approved!"
        message = (
            f"Your application as a Hope Carrier has been approved!\n\n"
            f"You can now access your dashboard using the following credentials:\n"
            f"Username: {user.email}\n"
            f"Temporary Password: {temp_password}\n\n"
            f"Login here: {login_url}\n\n"
            "Please change your password after your first login for security purposes.\n\n"
            "Thank you for standing in the gap with us."
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return f"Approval email sent to {user.email}"
    except User.DoesNotExist:
        return f"User with ID {user_id} does not exist"
    except Exception as e:
        return f"Error sending approval email: {str(e)}"

@shared_task
def send_password_reset_email(email, reset_url):
    try:
        send_mail(
            "Password Reset Request",
            f"Use this link to reset your password: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return f"Password reset email sent to {email}"
    except Exception as e:
        return f"Error sending password reset email: {str(e)}"

@shared_task
def send_prayer_encouragement_email(to_email, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        return f"Encouragement email sent to {to_email}"
    except Exception as e:
        return f"Error sending encouragement email: {str(e)}"
