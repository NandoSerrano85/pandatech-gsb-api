from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.model_protos import UserModel, RegisterRequest, RegisterResponse, AuthResponse
from app.services.user_service import UserServicer
from database.db import get_db

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    user_service = UserServicer()
    result = user_service.register_user(db, user.username, user.password, user.email)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return RegisterResponse(**result['user'].__dict__)

@router.post("/login", response_model=AuthResponse)
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user_service = UserServicer()
    result = user_service.authenticate_user(db, username, password)
    if not result['success']:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return AuthResponse(access_token=result['token'], token_type="bearer")

@router.get("/users/{user_id}", response_model=UserModel)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserServicer()
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserModel(**user.__dict__)