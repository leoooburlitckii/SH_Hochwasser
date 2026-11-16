import os

# Fake DB settings so that "import settings" works without a .env file.
# The engine is created lazily, so no real connection is opened during tests.
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
