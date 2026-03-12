import os
import django
from pathlib import Path
import environ
import sys

def test_config(env_file_name):
    print(f"\n--- Testing with {env_file_name} ---")
    BASE_DIR = Path(__file__).resolve().parent
    env = environ.Env()
    
    env_path = os.path.join(BASE_DIR, env_file_name)
    if not os.path.exists(env_path):
        print(f"❌ Error: {env_file_name} not found at {env_path}")
        return
        
    environ.Env.read_env(env_path)
    
    # Force settings based on the env file we're testing
    django_env = env('ENVIRONMENT', default='production')
    settings_module = 'config.settings.prod' if env_file_name == '.env.production' else 'config.settings.dev'
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    
    print(f"Using settings: {settings_module}")
    print(f"Email Host: {env('EMAIL_HOST', default='Not set')}")
    print(f"Email User: {env('EMAIL_HOST_USER', default='Not set')}")
    print(f"Default From: {env('DEFAULT_FROM_EMAIL', default='Not set')}")
    
    # Initialize Django
    try:
        # Reset django settings if already initialized
        from django.conf import settings
        import django
        django.setup()
    except Exception as e:
        print(f"Error during Django setup: {e}")

    from django.core.mail import send_mail
    
    recipient = "maricmarfil@gmail.com"
    subject = f"Test Email ({env_file_name})"
    
    try:
        print(f"Attempting to send direct email to {recipient}...")
        res = send_mail(
            subject=subject,
            message=f"This test verifies if {env_file_name} credentials work.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        if res:
            print(f"✅ SUCCESS! Email sent using {env_file_name} settings.")
        else:
            print(f"⚠️ FAILED. send_mail returned 0.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == '__main__':
    # Test both to see the difference
    test_config('.env')
    test_config('.env.production')
