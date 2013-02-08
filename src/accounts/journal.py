'''
Created on Dec 18, 2012

@author: thospy
'''
from libs import Database, Base, BaseModel

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import relationship, backref, deferred, validates


class Journal(BaseModel, Base):

    __tablename__ = "journalentries"
    
    id = Column(Integer, primary_key=True)
     
    accountDebit_id = Column(Integer, ForeignKey("accounts.id"))
    #accountDebit = relationship("Account",backref=backref("debitJournalEntries", order_by=id))
    accountCredit_id = Column(Integer, ForeignKey("accounts.id"))
    #accountCredit = relationship("Account",backref=backref("creditJournalEntries", order_by=id))
    
    amount = Column(Float)
    text = Column(String)
    
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document",backref=backref("journalentries", order_by=id))
    
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant",backref=backref("journalentries", order_by=id))

event.listen(Journal, 'before_insert', Journal.gen_tenant_id)
event.listen(Journal, 'before_update', Journal.gen_tenant_id)