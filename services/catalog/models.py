from __future__ import annotations
from decimal import Decimal
from threading import Lock
from typing import Dict, List, Optional
from common.schemas import Item, ItemCreate

class InMemoryCatalog:
    """Thread-safe in-memory item store for demo only."""
    def __init__(self) -> None:
        self._lock = Lock()
        self._seq = 0
        self._items: Dict[int, Item] = {}
        # Seed a couple of items
        self.create(ItemCreate(name="Coffee", price=Decimal("199.00")))
        self.create(ItemCreate(name="Tea", price=Decimal("99.50")))

    def list(self) -> List[Item]:
        with self._lock:
            return list(self._items.values())

    def get(self, item_id: int) -> Optional[Item]:
        with self._lock:
            return self._items.get(item_id)

    def create(self, payload: ItemCreate) -> Item:
        with self._lock:
            self._seq += 1
            item = Item(id=self._seq, name=payload.name, price=payload.price)
            self._items[item.id] = item
            return item

store = InMemoryCatalog()