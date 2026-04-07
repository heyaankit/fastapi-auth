"""Database configuration with async SQLAlchemy."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with async_session_maker() as session:
        yield session


sync_engine = None
sync_session_maker = None


def init_sync_db(database_url: str):
    global sync_engine, sync_session_maker
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    sync_engine = create_engine(database_url, pool_pre_ping=True)
    sync_session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)
