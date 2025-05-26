import jwt
import bcrypt
from datetime import datetime, timedelta

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# async def authenticate_user(self, db: AsyncSession, login: str, password: str) -> UserInDB | None:
#     user = await cruds.get_user(db, login)
#     if not user or not pwd_context.verify(password, user.password_hash):
#         return None
#     return user

# def create_access_token(self, data: TokenData, expires_delta: timedelta) -> str:
#     to_encode = data.model_dump()
#     expire = datetime.now(timezone.utc) + expires_delta
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    
# SECRET_KEY = "secret"
# ALGORITHM = "HS256"

# security = HTTPBearer()

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")