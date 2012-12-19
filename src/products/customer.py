'''
Created on Dec 19, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Customer(BaseModel, Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)