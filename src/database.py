from sqlalchemy import create_engine, Column, String, Integer, Boolean
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
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"User(id={self.id},first_name={self.first_name},last_name={self.last_name},age={self.age})"

Base.metadata.create_all(engine)

# Creating an instance of session to control
# db commands
# """
session = SessionLocal()
# """

# Inseting one value
"""
james = User(first_name="James", age=33)
session.add(james)
session.commit()
"""

# Inseting multiple values
"""
nick = User(first_name="Nick", age=26)
paul = User(first_name="Paul", age=42)
session.add_all([nick, paul])
session.commit()
"""

# Retrieve and update values
"""
found_user = session.query(User).filter_by(first_name="James").first()
if found_user is not None:
    found_user.last_name = "Brown"
    session.commit()
"""

# Query database using filter() or where() to use comparison
"""
users_filtered = session.query(User).filter(User.age >=25).all()
users_filtered = session.query(User).filter(User.age >=25,User.name == "ali").all()
users_filtered = session.query(User).where(User.age >=25,User.name == "ali").all()
"""

# Query using regex
"""
# users with similar name contianing specific substrings
users_similar_name = session.query(User).filter(User.name.like("%ali%")).all()

# users with case insensitive match
users_similar_name = session.query(User).filter(User.name.ilike("%ali%")).all()

# users with starting and ending chars
users_starting_ali = session.query(User).filter(User.name.like("Ali%")).all()
users_ending_ali = session.query(User).filter(User.name.like("%Ali")).all()
"""

# Use sentential logic
"""
from sqlalchemy import or_, and_, not_

# query those who has ali as name or age above 25
users_filtered = session.query(User).filter(or_(User.age >=25,User.name == "ali")).all()

# query those who has ali as name and age above 25
users_filtered = session.query(User).filter(and_(User.age >=25,User.name == "ali")).all()

# query those whos name is not ali
users_filtered = session.query(User).filter(not_(User.name == "ali")).all()

# getting users which are note named ali or age between 35,60
users = session.query(User).filter(or_(not_(User.name == "ali"),and_(User.age >35,User.age<60))
"""

session.close()
