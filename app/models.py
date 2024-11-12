from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer,  index=True)
    date = Column(DateTime, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    category = Column(String)

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    analytics = Column(String)