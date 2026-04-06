import os
import sys

def main():
    try:
        import environ
        from pathlib import Path
        import django
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please ensure you are running this in the project's virtual environment.")
        sys.exit(1)

    # Setup the exact same way as manage.py does
    BASE_DIR = Path(__file__).resolve().parent
    env = environ.Env()
    env_file = os.path.join(BASE_DIR, '.env')
    
    if os.path.exists(env_file):
        print(f"Loading environment from {env_file}")
        environ.Env.read_env(env_file)
    else:
        print(f"Warning: {env_file} not found. Defaulting to system environment variables.")

    # Determine settings module based on ENVIRONMENT variable
    django_env = env('ENVIRONMENT', default='production')
    settings_module = 'config.settings.prod' if django_env == 'production' else 'config.settings.dev'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    
    print(f"Using Django settings: {settings_module}")
    
    # Initialize Django
    django.setup()

    from django.core.mail import send_mail
    from django.conf import settings
    import logging

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("test_email")

    recipient = "maricmarfil@gmail.com"
    subject = "HopeBegins - Test Email from Server"
    message = "This is a test email sent from the server terminal to verify SMTP email configuration."

    logger.info(f"--- Email Configuration ---")
    logger.info(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
    logger.info(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    logger.info(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
    logger.info(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
    logger.info(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
    logger.info(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    logger.info(f"---------------------------")
    
    logger.info(f"Attempting to send an email to: {recipient}")
    
    try:
        res = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        if res:
            logger.info(f"SUCCESS! Sent test email to {recipient}.")
        else:
            logger.warning("FAILED. send_mail returned 0, meaning no email was sent.")
    except Exception as e:
        logger.error(f"ERROR: Failed to send email due to an exception.", exc_info=True)

if __name__ == '__main__':
    main()
