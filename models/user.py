from sqlalchemy import Column, Integer, String

from db.session import Base


# username: str
# avatar: Optional[str] = None
# phone: Optional[str] = None
# email: Optional[str] = None
class User(Base):
    # table name
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True,unique=True, nullable=False)
    avatar = Column(String)
    phone = Column(String)
    email = Column(String)
    hashed_password = Column(String, nullable=False)



