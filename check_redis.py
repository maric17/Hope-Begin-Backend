import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    print("Ping Redis:", r.ping())
    keys = r.keys()
    print("Keys in Redis:")
    for key in keys:
        if r.type(key) == b'list':
            qlen = r.llen(key)
            print(f"- {key}: {qlen} items")
        else:
            print(f"- {key}: type={r.type(key)}")
except Exception as e:
    print("Error connecting to Redis:", e)
