# db_service/app/grpc_order_server.py
import grpc
from concurrent import futures
from shared.generated import orders_pb2, orders_pb2_grpc
from app.database import get_db
from app.models import Order
from datetime import datetime, timezone


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        db = next(get_db())
        order = Order(
            user_id=request.user_id,
            item_name=request.item_name,
            price=request.price,
            status="pending",
            created_at=datetime.now(timezone.utc)
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        return orders_pb2.OrderResponse(
            order=orders_pb2.Order(
                id=order.id,
                user_id=order.user_id,
                item_name=order.item_name,
                price=order.price,
                status=order.status,
                created_at=order.created_at.isoformat()
            )
        )

    def ListOrdersByUser(self, request, context):
        db = next(get_db())
        orders = db.query(Order).filter(Order.user_id == request.user_id).all()
        return orders_pb2.OrderListResponse(
            orders=[
                orders_pb2.Order(
                    id=o.id,
                    user_id=o.user_id,
                    item_name=o.item_name,
                    price=o.price,
                    status=o.status,
                    created_at=o.created_at.isoformat()
                )
                for o in orders
            ]
        )

    def ListAllOrders(self, request, context):
        db = next(get_db())
        orders = db.query(Order).all()
        return orders_pb2.OrderListResponse(
            orders=[
                orders_pb2.Order(
                    id=o.id,
                    user_id=o.user_id,
                    item_name=o.item_name,
                    price=o.price,
                    status=o.status,
                    created_at=o.created_at.isoformat()
                )
                for o in orders
            ]
        )

def serve_orders():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port("[::]:50052")
    print("🟢 gRPC OrderService started on port 50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_orders()