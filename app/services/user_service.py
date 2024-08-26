import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token

class UserService:
    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(stored_password: bytes, provided_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def register_user(self, db: Session, username: str, password: str, email: str):
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return {'success': False, 'message': "Username already exists"}
        
        hashed_password = self.hash_password(password)
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {'success': True, 'message': "User registered successfully", 'user': new_user}

    def authenticate_user(self, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        
        if not user or not self.verify_password(user.hashed_password, password):
            return {'success': False, 'message': "Invalid username or password"}
        
        access_token = create_access_token(data={"sub": user.username})
        return {'success': True, 'message': "Authentication successful", 'token': access_token}

    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()