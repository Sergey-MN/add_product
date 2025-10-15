import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, CheckConstraint, Float, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, engine


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    orders_assoc: Mapped[list["OrdersProducts"]] = relationship(back_populates="product")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
        CheckConstraint("price > 0", name="check_price_positive"),
    )


class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"))
    products_assoc: Mapped[list["OrdersProducts"]] = relationship(back_populates="order")
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class OrdersProducts(Base):
    __tablename__ = "orders_products"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_order_quantity_positive"),
    )

    order: Mapped["Orders"] = relationship(back_populates="products_assoc")
    product: Mapped["Products"] = relationship(back_populates="orders_assoc")


class CategoryTree(Base):
    __tablename__ = "category_tree"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    supercategory_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category_tree.id"), nullable=True)
    supercategory: Mapped[Optional["CategoryTree"]] = relationship(back_populates="subcategory", remote_side=[id, ])
    subcategory: Mapped[list["CategoryTree"]] = relationship("CategoryTree", back_populates="supercategory")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
