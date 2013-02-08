'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel, Esr
from documentposition import Documentposition
from product import Product

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy import event
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property


class Document(BaseModel, Base):
    OFFER = 1
    BILL = 2
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True)
    partner_id = Column(Integer, ForeignKey("partners.id"))
    partner = relationship("Partner",backref=backref("documents", order_by=id))
    reference = Column(String, unique=True)
    type = Column(Integer)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant",backref=backref("documents", order_by=id))

    #referencenumber = Column(String, unique=True)
    
    
    
    @hybrid_property
    def referencenumber(self):
        return str(self.id)
    
    def esr(self):
                return Esr(amount=self.sum(), reference=self.referencenumber, account="01-4516-7")
    
    def sum(self):
        db = Database.instance()
        return float(db.session.query(Documentposition, func.sum((Product.price/100*(100-Documentposition.deduction)) * Documentposition.quantity))
            .join(Product)
            .filter(Documentposition.document_id==self.id)
            .all()[0][1])

event.listen(Document, 'before_insert', Document.gen_tenant_id)
event.listen(Document, 'before_update', Document.gen_tenant_id)
