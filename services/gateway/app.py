from __future__ import annotations
import os
from fastapi import FastAPI, HTTPException
import httpx
from common.schemas import Health

SERVICE = "gateway"
VERSION = os.getenv("APP_VERSION", "0.1.0")
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog:8000")
ORDERS_URL = os.getenv("ORDERS_URL", "http://orders:8001")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "2.5"))

app = FastAPI(title="API Gateway")

@app.get("/health", response_model=Health)
async def health() -> Health:
    return Health(service=SERVICE, version=VERSION)

@app.get("/api/items")
async def list_items():
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        r = await client.get(f"{CATALOG_URL}/items")
        r.raise_for_status()
        return r.json()

@app.post("/api/orders")
async def create_order(payload: dict):
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        r = await client.post(f"{ORDERS_URL}/orders", json=payload)
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail=r.json().get("detail"))
        r.raise_for_status()
        return r.json()