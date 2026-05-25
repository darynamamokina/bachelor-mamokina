from sqlalchemy import Column, Integer, String, Float
from database import Base

title = Column(String, nullable=False)
description = Column(String, nullable=True) 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    category = Column(String, nullable=True)  
    style = Column(String, nullable=True)     
    color = Column(String, nullable=True)
    gender = Column(String, nullable=True)    
    size = Column(String, nullable=True)
    material = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    store = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    product_url = Column(String, nullable=True)
    