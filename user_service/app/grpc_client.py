import grpc
from shared.generated import user_pb2, user_pb2_grpc

channel = grpc.insecure_channel("db_service:50051")
stub = user_pb2_grpc.UserServiceStub(channel)

def get_user_by_email(email: str):
    request = user_pb2.GetUserByEmailRequest(email=email)
    return stub.GetUserByEmail(request)

def get_user_by_id(user_id: int):
    request = user_pb2.UserIdRequest(id=user_id)
    return stub.GetUserById(request)

def create_user(username: str, email: str, password: str, role: str = "USER"):
    request = user_pb2.UserCreateRequest(
        username=username,
        email=email,
        hashed_password=password,
        role=role
    )
    return stub.CreateUser(request)

def list_users():
    return stub.ListUsers(user_pb2.Empty())
