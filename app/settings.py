import os

SECRET_KEY = os.getenv("SECRET_KEY", "jkorijshfueya526jh3sw3748jdnywhd")
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

ENV = os.getenv("ENV", "development")
