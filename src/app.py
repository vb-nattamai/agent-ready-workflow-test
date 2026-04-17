"""Order Service — minimal Flask API."""
from flask import Flask, jsonify, request, abort
from .models import OrderStore, Order

app = Flask(__name__)
store = OrderStore()


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/orders")
def create_order():
    body = request.get_json(silent=True) or {}
    customer_id = body.get("customer_id")
    items = body.get("items", [])
    if not customer_id:
        abort(400, "customer_id is required")
    if not items:
        abort(400, "items must not be empty")
    order = store.create(customer_id=customer_id, items=items)
    return jsonify(order.to_dict()), 201


@app.get("/orders/<order_id>")
def get_order(order_id):
    order = store.get(order_id)
    if order is None:
        abort(404, f"Order {order_id} not found")
    return jsonify(order.to_dict())


@app.get("/orders")
def list_orders():
    customer_id = request.args.get("customer")
    if not customer_id:
        abort(400, "customer query param is required")
    orders = store.list_by_customer(customer_id)
    return jsonify([o.to_dict() for o in orders])


@app.patch("/orders/<order_id>/cancel")
def cancel_order(order_id):
    order = store.get(order_id)
    if order is None:
        abort(404, f"Order {order_id} not found")
    if order.status == "cancelled":
        abort(409, "Order is already cancelled")
    order.status = "cancelled"
    return jsonify(order.to_dict())
