import grpc
from concurrent import futures
from pythonProtos.user_pb2 import UserRequest, UserResponse, RegisterResponse, AuthResponse
from pythonProtos.user_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server
from app.services.user_service import UserService
from database.db import engine, Base, get_db
from app.core.config import settings

class GRPCUserService(UserServiceServicer):
    def __init__(self):
        self.user_service = UserService()

    def RegisterUser(self, request, context):
        db = next(get_db())
        result = self.user_service.register_user(db, request.username, request.password, request.email)
        if not result['success']:
            return RegisterResponse(success=False, message=result['message'])
        return RegisterResponse(success=True, message=result['message'], user_id=result['user'].id)

    def AuthenticateUser(self, request, context):
        db = next(get_db())
        result = self.user_service.authenticate_user(db, request.username, request.password)
        if not result['success']:
            return AuthResponse(success=False, message=result['message'])
        return AuthResponse(success=True, message=result['message'], token=result['token'])

    def GetUser(self, request, context):
        db = next(get_db())
        user = self.user_service.get_user(db, request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return UserResponse()
        return UserResponse(id=user.id, username=user.username, email=user.email)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(GRPCUserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    serve()