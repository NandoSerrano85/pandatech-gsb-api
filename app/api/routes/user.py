from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import UserService
from database.db import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService()
    result = user_service.register_user(db, user.username, user.password, user.email)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return UserResponse(**result['user'].__dict__)

@router.post("/login", response_model=Token)
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user_service = UserService()
    result = user_service.authenticate_user(db, username, password)
    if not result['success']:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return Token(access_token=result['token'], token_type="bearer")

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService()
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.__dict__)