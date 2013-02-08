'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Tenant(BaseModel, Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    esr_account = Column(String, unique=True)
    esr_reference_prefix = Column(String, unique=True)
