import os
import django
from pathlib import Path
import environ

def main():
    BASE_DIR = Path(__file__).resolve().parent
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    
    django_env = env('ENVIRONMENT', default='production')
    settings_module = 'config.settings.prod' if django_env == 'production' else 'config.settings.dev'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    
    print(f"Using settings: {settings_module}")
    django.setup()
    
    from apps.users.tasks import send_approval_email
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    # Find a user to test with, or just use a dummy email if we can bypass the DB check
    # The task send_approval_email does: user = User.objects.get(id=user_id)
    # Let's check for users.
    user = User.objects.first()
    if not user:
        print("No users found in database!")
        return
        
    print(f"Testing send_approval_email for user: {user.email}")
    result = send_approval_email.delay(user.id, "TestPassword123")
    print(f"Task triggered. Result ID: {result.id}")
    
    # If ALWAYS_EAGER is True, it will have run already and we should see output.
    # If False, it went to Redis.

if __name__ == '__main__':
    main()
