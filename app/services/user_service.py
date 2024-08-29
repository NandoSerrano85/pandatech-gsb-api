import bcrypt, grpc
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token
from database.db import get_db

from pythonProtos.user_pb2 import (
    RegisterResponse,
    AuthResponse,
    UserResponse,
)
from pythonProtos.user_pb2_grpc import UserServiceServicer

class UserServicer(UserServiceServicer):
    def RegisterUser(self, request, context):
        db = next(get_db())
        result = self._register_user(db, request.username, request.password, request.email)
        if not result['success']:
            return RegisterResponse(success=False, message=result['message'])
        return RegisterResponse(success=True, message=result['message'], user_id=result['user'].id)

    def AuthenticateUser(self, request, context):
        db = next(get_db())
        result = self._authenticate_user(db, request.username, request.password)
        if not result['success']:
            return AuthResponse(success=False, message=result['message'])
        return AuthResponse(success=True, message=result['message'], token=result['token'])

    def GetUser(self, request, context):
        db = next(get_db())
        user = self._get_user(db, request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return UserResponse()
        return UserResponse(id=user.id, username=user.username, email=user.email)
    
    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def _verify_password(self, stored_password: bytes, provided_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def _register_user(self, db: Session, username: str, password: str, email: str):
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return {'success': False, 'message': "Username already exists"}
        
        hashed_password = self._hash_password(password)
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {'success': True, 'message': "User registered successfully", 'user': new_user}

    def _authenticate_user(self, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        
        if not user or not self._verify_password(user.hashed_password, password):
            return {'success': False, 'message': "Invalid username or password"}
        
        access_token = create_access_token(data={"sub": user.username})
        return {'success': True, 'message': "Authentication successful", 'token': access_token}

    def _get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()