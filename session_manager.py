from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
SALT = os.environ.get("SALT", "mysalt")

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_token(user_id):
    return serializer.dumps(user_id, salt=SALT)

def verify_token(token, max_age=3600):
    try:
        user_id = serializer.loads(token, salt=SALT, max_age=max_age)
        print(f"Token verified, user ID: {user_id}")
        return user_id
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None