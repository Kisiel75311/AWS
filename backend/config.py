import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "your-jwt-secret-key"  # JWT Secret Key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Optional: Configure the duration of JWT access tokens

