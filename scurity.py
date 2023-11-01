from passlib.context import CryptContext  # pip install passlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # pip install bcrypt


# password hash
def get_password_hash(password):
    return pwd_context.hash(password)
