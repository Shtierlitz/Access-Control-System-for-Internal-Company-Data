# admin_service/app/grpc_clients/user.py
import grpc
from shared.generated import user_pb2, user_pb2_grpc

channel = grpc.insecure_channel("db_service:50051")

stub = user_pb2_grpc.UserServiceStub(channel)

def list_users():
    response = stub.ListUsers(user_pb2.Empty())
    return [
        {
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "role": u.role
        } for u in response.users
    ]

def get_user_by_id(user_id: int):
    request = user_pb2.UserIdRequest(id=user_id)
    response = stub.GetUserById(request)

    return {
        "id": response.id,
        "email": response.email,
        "username": response.username,
        "role": response.role,
    }