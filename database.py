from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    # echo=True,
)

session = async_sessionmaker(bind=engine)


async def get_session():
    async with session() as local_session:
        yield local_session


class Base(DeclarativeBase):
    pass
