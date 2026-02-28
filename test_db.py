import psycopg2
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

try:
    print(f"Connecting to {env('DB_HOST')} on port {env('DB_PORT')} as {env('DB_USER')}...")
    conn = psycopg2.connect(
        dbname=env('DB_NAME'),
        user=env('DB_USER'),
        password=env('DB_PASSWORD'),
        host=env('DB_HOST'),
        port=env('DB_PORT'),
        sslmode='require'
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
