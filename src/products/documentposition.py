'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Documentposition(BaseModel, Base):
    __tablename__ = "documentpositions"
    
    id = Column(Integer, primary_key=True)
    deduction = Column(Float)
    quantity = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product",backref=backref("documentpositions", order_by=id))

    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document",backref=backref("documentpositions", order_by=id))
