from typing import Any

from fastapi import FastAPI, Body
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()

ITEMS = set()


class ItemModel(BaseModel):
    pk: str
    name: str
    data: dict[str, Any] | None

    def __hash__(self) -> int:
        return hash(self.pk)


@app.get("/")
async def home():
    return {"message": "ok"}


@app.post("/item")
async def add_item(item: ItemModel = Body()):
    ITEMS.add(item)
    return {"message": "ok"}


@app.get("/item", response_model=list[ItemModel])
async def get_items():
    return list(ITEMS)

    
lambda_handler = Mangum(app, lifespan="off")