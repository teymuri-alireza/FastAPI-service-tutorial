from sqlalchemy import create_engine, Column, String, Integer
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=True)
    age = Column(Integer)

    def __repr__(self):
        return f"User(id={self.id},first_name={self.first_name},last_name={self.last_name},age={self.age})"

Base.metadata.create_all(engine)
