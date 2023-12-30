
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") #hashing algorithm to hide passwords

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password,hash_password):
    return pwd_context.verify(plain_password,hash_password)