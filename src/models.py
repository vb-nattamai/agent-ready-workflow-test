"""Domain models for the Order Service."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Order:
    id: str
    customer_id: str
    items: list[dict[str, Any]]
    status: str = "pending"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "items": self.items,
            "status": self.status,
            "created_at": self.created_at,
        }


class OrderStore:
    """In-memory order store. Replace with a real DB in production."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def create(self, customer_id: str, items: list[dict[str, Any]]) -> Order:
        order = Order(id=str(uuid.uuid4()), customer_id=customer_id, items=items)
        self._orders[order.id] = order
        return order

    def get(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def list_by_customer(self, customer_id: str) -> list[Order]:
        return [o for o in self._orders.values() if o.customer_id == customer_id]
