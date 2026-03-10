# Redis Troubleshooting Guide

This guide explains how to verify if Redis is working correctly on the server. Redis is used as the message broker for Celery and for caching.

## 1. Check Redis Service Status (Linux/Ubuntu)

Most production servers use `systemd` to manage Redis. Run the following command to see if it's active:

```bash
sudo systemctl status redis
# OR if it's named redis-server
sudo systemctl status redis-server
```

**What to look for:**
- `Active: active (running)` means it's working.
- `Active: inactive (dead)` or `failed` means it's stopped.

**To Start/Restart:**
```bash
sudo systemctl start redis
sudo systemctl restart redis
```

---

## 2. Test Connection using `redis-cli`

The fastest way to test if Redis is responding is using the built-in CLI tool.

### Ping Test
```bash
redis-cli ping
```
**Expected Result:** `PONG`

### Check Connection Details
If Redis is running on a non-default port or requires a password (check your `.env` file):
```bash
redis-cli -h localhost -p 6379 ping
```

---

## 3. Run the Python Test Script

In the root of the project, there is a specialized script `test_redis.py` that checks the connection using the actual environment variables from your `.env` file.

```bash
# Activate your virtual environment first
source venv/bin/activate

# Run the test script
python test_redis.py
```

**Example output of a successful test:**
```text
Connecting to Redis at redis://localhost:6379/0...
✅ Redis PING successful! Connection established.
✅ Data write/read test successful!
```

---

## 4. Check Redis Logs

If Redis isn't starting or is behaving unexpectedly, check the system logs:

```bash
sudo journalctl -u redis-server -f
# OR check the log file directly
sudo tail -f /var/log/redis/redis-server.log
```

---

## 5. Verify App Configuration

Ensure your `.env.production` or `.env` file has the correct `CELERY_BROKER_URL`:

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## 6. Environment Selection

The project automatically switches between Development and Production settings based on the `ENVIRONMENT` variable in your `.env` file:

- **Local Development**: Set `ENVIRONMENT=development` in `.env` to use `config.settings.dev`.
- **Production Server**: Set `ENVIRONMENT=production` in `.env` to use `config.settings.prod`.

This variable is read by `manage.py`, `wsgi.py`, and `celery.py` to decide which configuration to load.
