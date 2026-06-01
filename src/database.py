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

# COMMANDS DOCUMENTATION

# Creating an instance of session to control
# db commands
# """
# session = SessionLocal()
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

# Use aggregation for complex queries
"""
from sqlalchemy import func

# 1. Count Total Users
total_users = session.query(func.count(User.id)).scalar()
print("Total Users:", total_users)

# 2. Find the Average Age of Users
average_age = session.query(func.avg(User.age)).scalar()
print("Average Age:", average_age)

# 3. Find the Maximum and Minimum Age
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()
print(f"Max Age: {max_age}, Min Age: {min_age}")

# 4. Find the Total Number of Orders
total_orders = session.query(func.count(Order.id)).scalar()
print("Total Orders:", total_orders)

# 5. Find the Sum of All Order Amounts
total_revenue = session.query(func.sum(Order.total_amount)).scalar()
print("Total Revenue:", total_revenue)

# 6. Find the Average Order Value
average_order_value = session.query(func.avg(Order.total_amount)).scalar()
print("Average Order Value:", average_order_value)

# 7. Find Users Who Have Placed the Most Orders
most_active_users = session.query(
    User.name, func.count(Order.id).label("order_count")
).join(Order).group_by(User.id).order_by(func.count(Order.id).desc()).limit(5).all()
print("Top 5 Active Users by Order Count:", most_active_users)

# 8. Find Users with the Highest Total Spending
top_spenders = session.query(
    User.name, func.sum(Order.total_amount).label("total_spent")
).join(Order).group_by(User.id).order_by(func.sum(Order.total_amount).desc()).limit(5).all()
print("Top 5 Users by Spending:", top_spenders)

# 9. Find Users Who Have Not Placed Any Orders
users_without_orders = session.query(User).outerjoin(Order).filter(Order.id == None).all()
print("Users Without Orders:", [user.name for user in users_without_orders])

# 10. Find the Most Recent Order Date
latest_order_date = session.query(func.max(Order.created_at)).scalar()
print("Most Recent Order Date:", latest_order_date)
"""

# session.close()
