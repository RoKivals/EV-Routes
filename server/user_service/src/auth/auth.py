from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from jose import jwt

from database.schemas import UserInDB, TokenData
from database import cruds

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm

    async def authenticate_user(self, db: AsyncSession, login: str, password: str) -> UserInDB | None:
        user = await cruds.get_user(db, login)
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user

    def create_access_token(self, data: TokenData, expires_delta: timedelta) -> str:
        to_encode = data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)