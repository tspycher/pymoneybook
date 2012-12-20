'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel
from documentposition import Documentposition
from product import Product

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Document(BaseModel, Base):
    OFFER = 1
    BILL = 2
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer",backref=backref("documents", order_by=id))

    type = Column(Integer)
    
    def sum(self):
        db = Database.instance()
        return float(db.session.query(Documentposition, func.sum((Product.price/100*(100-Documentposition.deduction)) * Documentposition.quantity))
            .join(Product)
            .filter(Documentposition.document_id==self.id)
            .all()[0][1])
