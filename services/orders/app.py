from __future__ import annotations
import os
from decimal import Decimal
from fastapi import FastAPI, HTTPException
import httpx
from common.schemas import Order, OrderCreate, Health, Item
from .models import store

SERVICE = "orders"
VERSION = os.getenv("APP_VERSION", "0.1.0")
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog:8000")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "2.5"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "2"))

app = FastAPI(title="Orders Service")

@app.get("/health", response_model=Health)
async def health() -> Health:
    return Health(service=SERVICE, version=VERSION)

async def get_item_safe(item_id: int) -> Item:
    last_exc: Exception | None = None
    for _ in range(RETRY_ATTEMPTS + 1):
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                resp = await client.get(f"{CATALOG_URL}/items/{item_id}")
                if resp.status_code == 404:
                    raise HTTPException(status_code=404, detail="Item not found in catalog")
                resp.raise_for_status()
                return Item(**resp.json())
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
    # Simple fail-fast after retries
    raise HTTPException(status_code=502, detail=f"Catalog lookup failed: {last_exc}")

@app.post("/orders", response_model=Order, status_code=201)
async def create_order(payload: OrderCreate) -> Order:
    item = await get_item_safe(payload.item_id)
    return store.create(payload, price=Decimal(str(item.price)))

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int) -> Order:
    order = store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order