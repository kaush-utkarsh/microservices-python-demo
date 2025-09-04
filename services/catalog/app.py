from __future__ import annotations
import os
from fastapi import FastAPI, HTTPException
from common.schemas import Item, ItemCreate, Health
from .models import store

SERVICE = "catalog"
VERSION = os.getenv("APP_VERSION", "0.1.0")

app = FastAPI(title="Catalog Service")

@app.get("/health", response_model=Health)
async def health() -> Health:
    return Health(service=SERVICE, version=VERSION)

@app.get("/items", response_model=list[Item])
async def list_items() -> list[Item]:
    return store.list()

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    item = store.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=201)
async def create_item(payload: ItemCreate) -> Item:
    return store.create(payload)