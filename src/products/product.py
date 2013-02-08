'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Product(BaseModel, Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    number = Column(String, unique=True)
    price = Column(Float)
    description = Column(String)
    
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant",backref=backref("products", order_by=id))

event.listen(Product, 'before_insert', Product.gen_tenant_id)
event.listen(Product, 'before_update', Product.gen_tenant_id)