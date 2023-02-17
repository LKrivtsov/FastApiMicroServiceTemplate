from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from db.base_class import Base
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    middlename = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    is_email_confirmed = Column(Boolean)
    email_confirmed_at = Column(DateTime)
    phone = Column(String)
    iin = Column(String)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)
    created_at = Column(DateTime)
    last_seen_at = Column(DateTime)
    id_card = Column(String)
    is_phone_confirmed = Column(Boolean)
    phone_confirmed_at = Column(DateTime)
