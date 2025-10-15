import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas import FeedBack
from services import add_product_to_order

app = FastAPI()


@app.post("/orders/{order_id}", status_code=201, response_model=FeedBack)
async def add_item(order_id: int, product_id: int, quantity: int, session: AsyncSession = Depends(get_session)):
    return await add_product_to_order(order_id, product_id, quantity, session)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
