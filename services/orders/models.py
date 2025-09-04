from __future__ import annotations
from decimal import Decimal
from threading import Lock
from typing import Dict, Optional
from common.schemas import Order, OrderCreate

class InMemoryOrders:
    def __init__(self) -> None:
        self._lock = Lock()
        self._seq = 0
        self._orders: Dict[int, Order] = {}

    def create(self, payload: OrderCreate, price: Decimal) -> Order:
        total = (price * Decimal(payload.qty)).quantize(Decimal("0.01"))
        with self._lock:
            self._seq += 1
            order = Order(id=self._seq, item_id=payload.item_id, qty=payload.qty, total=total)
            self._orders[order.id] = order
            return order

    def get(self, order_id: int) -> Optional[Order]:
        with self._lock:
            return self._orders.get(order_id)

store = InMemoryOrders()