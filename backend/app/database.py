from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


# Configure connection arguments based on database type
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(settings.database_url, connect_args=connect_args)
elif settings.database_url.startswith("postgresql"):
    # PostgreSQL-specific configuration with connection pooling for Neon
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,  # Check connections before use
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_size=5,  # Reduced pool size for Neon
        max_overflow=10,  # Additional connections when pool is full
        pool_timeout=30,  # Timeout for getting connection from pool
        connect_args={
            "connect_timeout": 60,  # Connection timeout in seconds
            "sslmode": "require",  # Require SSL for Neon
            "application_name": "spotify_clone",
        },
    )
else:
    # Default configuration for other databases
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
