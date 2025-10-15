from pydantic import BaseModel


class FeedBack(BaseModel):
    order_id: int
    product_id: int
    added_quantity: int
