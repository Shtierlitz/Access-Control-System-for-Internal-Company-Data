# db_service/app/grpc_server.py
import grpc
from concurrent import futures

from shared.generated import user_pb2_grpc, user_pb2
from app.database import get_db
from app.models import User

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUserByEmail(self, request, context):
        db = next(get_db())
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        # noinspection PyUnresolvedReferences
        return user_pb2.UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            role=user.role,
            hashed_password=user.hashed_password
        )

    def GetUserById(self, request, context):
        db = next(get_db())
        user = db.query(User).filter(User.id == request.id).first()
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        # noinspection PyUnresolvedReferences
        return user_pb2.UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            role=user.role,
            hashed_password=user.hashed_password
        )

    def CreateUser(self, request, context):
        db = next(get_db())

        new_user = User(
            email=request.email,
            username=request.username,
            hashed_password=request.hashed_password,
            role=request.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # noinspection PyUnresolvedReferences
        return user_pb2.UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            role=new_user.role,
            hashed_password=new_user.hashed_password
        )

    def ListUsers(self, request, context):
        db = next(get_db())
        users = db.query(User).all()
        # noinspection PyUnresolvedReferences
        return user_pb2.UserListResponse(
            users=[
                user_pb2.UserResponse(
                    id=u.id,
                    email=u.email,
                    username=u.username,
                    role=u.role,
                    hashed_password=u.hashed_password
                )
                for u in users
            ]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    print("🟢 gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()