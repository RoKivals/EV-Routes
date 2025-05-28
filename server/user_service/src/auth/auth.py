from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
import jwt
from pydantic import SecretStr
from database.schemas import UserInDB, TokenData
from database import cruds

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm

    async def authenticate_user(self, db: AsyncSession, login: str, password: SecretStr) -> UserInDB | None:
        user = await cruds.get_user(db, login)
        password_orig = password.get_secret_value()
        if not user or not pwd_context.verify(password_orig, user.password_hash):
            return None
        return user

    def create_access_token(self, data: TokenData, expires_delta: timedelta) -> str:
        to_encode = data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    

# def decode_token(token: str):
#     return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])