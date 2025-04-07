from passlib.context import CryptContext # for password
#this is used to encode the password or can say convert the password into a 
# #hashed format to provide security 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(password: str):

    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    