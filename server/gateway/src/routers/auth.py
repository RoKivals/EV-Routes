from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from utils import hash_password, verify_password, create_access_token
import psycopg2

router = APIRouter()

SECRET_KEY = "secret"

conn = psycopg2.connect(dbname="evroutesusers", user="roki", password="roki", host="localhost")
cursor = conn.cursor()

class LoginData(BaseModel):
    email: EmailStr
    password: str

class RegisterData(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

@router.post("/register")
def register(data: RegisterData):
    cursor.execute("SELECT 1 FROM users WHERE email = %s", (data.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(data.password)

    cursor.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (%s, %s, %s)",
        (data.email, hashed_pw, data.role)
    )
    conn.commit()
    return {"status": "registered"}

@router.post("/login")
def login(data: LoginData):
    cursor.execute("SELECT password_hash, role FROM users WHERE email = %s", (data.email,))
    row = cursor.fetchone()
    if not row or not verify_password(data.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"email": data.email, "role": row[1]})
    return {"access_token": token}