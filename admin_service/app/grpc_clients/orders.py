# admin_service/app/grpc_clients/orders.py
import grpc
from shared.generated import orders_pb2, orders_pb2_grpc

channel = grpc.insecure_channel("db_service:50052")

stub = orders_pb2_grpc.OrderServiceStub(channel)

def get_all_orders():
    response = stub.ListAllOrders(orders_pb2.Empty())
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "item_name": o.item_name,
            "price": o.price,
            "status": o.status,
            "created_at": o.created_at
        } for o in response.orders
    ]

def get_orders_by_user(user_id: int):
    request = orders_pb2.UserIdRequest(user_id=user_id)
    response = stub.ListOrdersByUser(request)
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "item_name": o.item_name,
            "price": o.price,
            "status": o.status,
            "created_at": o.created_at
        } for o in response.orders
    ]