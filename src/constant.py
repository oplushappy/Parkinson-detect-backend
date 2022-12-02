from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

SECRET_KEY = open("./secret_key", "r").read()
ALGORITHM = "HS256" #算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #訪問令牌時間
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/jwt/token")
