'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Partner(BaseModel, Base):
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant",backref=backref("partners", order_by=id))

event.listen(Partner, 'before_insert', Partner.gen_tenant_id)
event.listen(Partner, 'before_update', Partner.gen_tenant_id)