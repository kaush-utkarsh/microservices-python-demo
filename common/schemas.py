# common/schemas.py
from __future__ import annotations
from pydantic import BaseModel, Field, PositiveInt, condecimal
from typing import Optional

class Item(BaseModel):
    id: PositiveInt
    name: str = Field(..., min_length=1, max_length=80)
    price: condecimal(gt=0, max_digits=10, decimal_places=2)

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    price: condecimal(gt=0, max_digits=10, decimal_places=2)

class OrderCreate(BaseModel):
    item_id: PositiveInt
    qty: PositiveInt

class Order(BaseModel):
    id: PositiveInt
    item_id: PositiveInt
    qty: PositiveInt
    total: condecimal(gt=0, max_digits=12, decimal_places=2)

class Health(BaseModel):
    status: str = "ok"
    service: str
    version: str
    note: Optional[str] = None