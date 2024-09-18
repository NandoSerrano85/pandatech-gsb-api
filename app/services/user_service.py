import bcrypt, grpc
from sqlalchemy.orm import Session
from app.models.model_protos import UserModel
from app.core.security import create_access_token
from database.db import get_db

from protos.generated.user_pb2 import (
    RegisterResponse,
    AuthResponse,
    User,
)
from protos.generated.user_pb2_grpc import UserServiceServicer

class UserServicer(UserServiceServicer):
    def RegisterUser(self, request, context):
        db = next(get_db())
        result = self._register_user(db, request.username, request.password, request.email, request.firstname, request.lastname, request.store_url, request.api_access_token)
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
            return User()
        return User(id=user.id, username=user.username, email=user.email)
    
    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def _verify_password(self, stored_password: bytes, provided_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def _register_user(self, db: Session, username: str, password: str, email: str, firstname: str, lastname: str, store_url: str, api_access_token: str):
        existing_user = db.query(UserModel).filter(UserModel.username == username).first()
        if existing_user:
            return {'success': False, 'message': "Username already exists"}
        
        hashed_password = self._hash_password(password)
        new_user = UserModel(username=username, email=email, hashed_password=hashed_password, firstname=firstname, lastname=lastname, store_url=store_url, api_access_token=api_access_token)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {'success': True, 'message': "User registered successfully", 'user': new_user}

    def _authenticate_user(self, db: Session, username: str, password: str):
        user = db.query(UserModel).filter(UserModel.username == username).first()
        
        if not user or not self._verify_password(user.hashed_password, password):
            return {'success': False, 'message': "Invalid username or password"}
        
        access_token = create_access_token(data={"sub": user.username})
        return {'success': True, 'message': "Authentication successful", 'token': access_token}

    def _get_user(self, db: Session, user_id: int):
        return db.query(UserModel).filter(UserModel.id == user_id).first()