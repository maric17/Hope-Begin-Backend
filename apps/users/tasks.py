from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task
def send_approval_email(user_id, temp_password):
    logger.info(f"Task send_approval_email triggered for user_id={user_id}")
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
        
        logger.info(f"Attempting to send approval email to {user.email}")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent approval email to {user.email}")
        return f"Approval email sent to {user.email}"
    except User.DoesNotExist:
        logger.warning(f"Failed to send approval email: User with ID {user_id} does not exist")
        return f"User with ID {user_id} does not exist"
    except Exception as e:
        logger.error(f"Error sending approval email to user_id={user_id}: {str(e)}", exc_info=True)
        return f"Error sending approval email: {str(e)}"

@shared_task
def send_password_reset_email(email, reset_url):
    logger.info(f"Task send_password_reset_email triggered for email={email}")
    try:
        logger.info(f"Attempting to send password reset email to {email}")
        send_mail(
            "Password Reset Request",
            f"Use this link to reset your password: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent password reset email to {email}")
        return f"Password reset email sent to {email}"
    except Exception as e:
        logger.error(f"Error sending password reset email to {email}: {str(e)}", exc_info=True)
        return f"Error sending password reset email: {str(e)}"

@shared_task
def send_prayer_encouragement_email(to_email, subject, message):
    logger.info(f"Task send_prayer_encouragement_email triggered for to_email={to_email}")
    try:
        logger.info(f"Attempting to send encouragement email to {to_email}")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent encouragement email to {to_email}")
        return f"Encouragement email sent to {to_email}"
    except Exception as e:
        logger.error(f"Error sending encouragement email to {to_email}: {str(e)}", exc_info=True)
        return f"Error sending encouragement email: {str(e)}"

@shared_task
def send_assignment_notification_email(carrier_email, prayer_title):
    logger.info(f"Task send_assignment_notification_email triggered for carrier_email={carrier_email}")
    try:
        login_url = f"{settings.FRONTEND_URL}/login/carrier"
        subject = "New Prayer Request Assigned to You!"
        message = (
            f"Hello,\n\n"
            f"An administrator has assigned a new prayer request to you: \"{prayer_title}\".\n\n"
            f"Please log in to your dashboard to view the details and start praying:\n"
            f"{login_url}\n\n"
            "Thank you for your faithful service."
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [carrier_email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent assignment email to {carrier_email}")
        return f"Assignment email sent to {carrier_email}"
    except Exception as e:
        logger.error(f"Error sending assignment email to {carrier_email}: {str(e)}", exc_info=True)
        return f"Error sending assignment email: {str(e)}"
