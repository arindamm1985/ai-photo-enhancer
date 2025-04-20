
import os
broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
result_backend = broker_url
