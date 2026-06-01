from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

database = "sqlite.db"

engine = create_engine(
    f"sqlite:///{database}",
    echo=False,
    future=True,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    """
    Used as the base for new declarative mappings
    """
    pass

Base.metadata.create_all(engine)
