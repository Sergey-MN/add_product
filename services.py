from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, InterfaceError, IntegrityError, InvalidRequestError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger import logger
from models import Orders, Products, OrdersProducts
from schemas import FeedBack

async def get_order(order_id: int, session:AsyncSession):
    order = await session.get(Orders, order_id)

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    return order

async def get_product(product_id: int, session:AsyncSession):
    product = await session.get(Products, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")
    return product

def check_quantity(product: Products, quantity: int):
    if product.quantity < quantity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Недостаточное количество на складе")




async def add_product_to_order(order_id: int, product_id: int, quantity: int, session: AsyncSession):
    try:
        order = await get_order(order_id, session)
        product = await get_product(product_id, session)

        check_quantity(product, quantity)

        stmt = select(OrdersProducts).where(OrdersProducts.order_id == order.id,
                                            OrdersProducts.product_id == product_id)
        res = await session.execute(stmt)
        product_order = res.scalar_one_or_none()

        product.quantity -= quantity
        if product_order:
            product_order.quantity += quantity
        else:
            session.add(OrdersProducts(order_id=order_id, product_id=product_id, quantity=quantity))
        await session.commit()

    except (OperationalError, InterfaceError) as e:
        await session.rollback()
        logger.error(f"Network error: {e}")
        raise RuntimeError("Database connection error") from e

    except IntegrityError as e:
        await session.rollback()
        logger.warning(f"Integrity violation: {e}")
        raise ValueError("Data integrity error") from e

    except (InvalidRequestError, SQLAlchemyError) as e:
        await session.rollback()
        logger.error(f"SQLAlchemy error: {e}")
        raise RuntimeError("SQLAlchemy error") from e

    except Exception as e:
        await session.rollback()
        logger.exception(f"Unexpected error: {e}")
        raise

    return FeedBack(
        order_id=order_id,
        product_id=product_id,
        added_quantity=quantity,
    )
