import grpc
from shared.generated import user_pb2, user_pb2_grpc
from shared.generated import orders_pb2, orders_pb2_grpc
from app.schemas import OrderCreate

# --- gRPC: UserService ---
user_channel = grpc.insecure_channel("db_service:50051")
user_stub = user_pb2_grpc.UserServiceStub(user_channel)

def get_user_by_email(email: str):
    # noinspection PyUnresolvedReferences
    request = user_pb2.GetUserByEmailRequest(email=email)
    return user_stub.GetUserByEmail(request)

# --- gRPC: OrderService ---
order_channel = grpc.insecure_channel("db_service:50052")
order_stub = orders_pb2_grpc.OrderServiceStub(order_channel)

def create_order_grpc(order: OrderCreate, user_id: int):
    # noinspection PyUnresolvedReferences
    request = orders_pb2.CreateOrderRequest(
        user_id=user_id,
        item_name=order.item_name,
        price=order.price
    )
    response = order_stub.CreateOrder(request)
    return response.order

def get_orders_for_user(user_id: int):
    # noinspection PyUnresolvedReferences
    request = orders_pb2.UserIdRequest(user_id=user_id)
    response = order_stub.ListOrdersByUser(request)
    return list(response.orders)

def get_all_orders_grpc():
    # noinspection PyUnresolvedReferences
    request = orders_pb2.Empty()
    response = order_stub.ListAllOrders(request)
    return list(response.orders)
