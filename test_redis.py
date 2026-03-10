import redis
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

redis_url = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')

try:
    print(f"Connecting to Redis at {redis_url}...")
    # Parse the URL (e.g., redis://localhost:6379/0)
    r = redis.from_url(redis_url)
    
    # Test connection with a PING
    if r.ping():
        print("✅ Redis PING successful! Connection established.")
        
        # Test writing and reading
        r.set('test_key', 'it works!')
        val = r.get('test_key')
        if val == b'it works!':
            print("✅ Data write/read test successful!")
            r.delete('test_key')
        else:
            print(f"❌ Data mismatch. Expected 'it works!', got '{val}'")
    else:
        print("❌ Redis PING failed.")

except Exception as e:
    print(f"❌ Connection failed: {e}")
