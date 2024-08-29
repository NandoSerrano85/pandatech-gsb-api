import grpc
from concurrent import futures
from pythonProtos.user_pb2_grpc import add_UserServiceServicer_to_server
from pythonProtos.images_pb2_grpc import add_ImageServiceServicer_to_server
from database.db import engine, Base
from app.services.user_service import UserServicer
from app.services.image_service import ImageServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(UserServicer(), server)
    add_ImageServiceServicer_to_server(ImageServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    serve()