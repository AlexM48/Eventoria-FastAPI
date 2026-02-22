from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://"
)
# else:
#     DATABASE_URL = (
#         f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
#         f"{settings.POSTGRES_PASSWORD}@"
#         f"{settings.POSTGRES_HOST}:"
#         f"{settings.POSTGRES_PORT}/"
#         f"{settings.POSTGRES_DB}"
#     )


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
