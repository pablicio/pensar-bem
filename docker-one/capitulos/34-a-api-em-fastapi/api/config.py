import os

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ.get("REDIS_URL", "redis://cache:6379/0")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info")
