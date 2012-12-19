'''
Created on Dec 18, 2012

@author: thospy

          Soll  Haben
Aktiven   +     -
Aufwand   +     -
Passiven  -     +
Ertrag    -     +
'''
from libs import Database, Base, BaseModel
from journal import Journal

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred, validates
from sqlalchemy.sql import func


class Account(BaseModel, Base):
    ACTIVE = 1
    PASSIVE = 2
    EXPENSE = 3
    AUFWAND = EXPENSE
    INCOME = 4
    ERTRAG = INCOME
    
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    number = Column(Integer)
    type = Column(Integer)
    
    def bookSoll(self, amount, otherAccount, text = None):
        return self.bookDebit(amount, otherAccount, text)
    
    def bookDebit(self, amount, otherAccount, text = None):
        return self._book(self, otherAccount, amount, text)
    
    def bookHaben(self,amount, otherAccount, text = None):
        return self.bookCredit(amount, otherAccount, text)
        
    def bookCredit(self, amount, otherAccount, text = None):
        return self._book(otherAccount, self, amount, text)
    
    def _book(self, debitAccount, creditAccount, amount, text):
        journal = Journal(accountDebit_id=debitAccount.id, accountCredit_id=creditAccount.id, amount=amount, text=text)
        journal.save()
        return journal
        
    def saldo(self):
        db = Database.instance()
        sumCredit = db.session.query(func.sum(Journal.amount)).filter(Journal.accountCredit_id==self.id).scalar()
        sumDebit = db.session.query(func.sum(Journal.amount)).filter(Journal.accountDebit_id==self.id).scalar()
        if not sumCredit: sumCredit = 0
        if not sumDebit: sumDebit = 0
        if self.type & 1:
            # odd
            total = sumDebit - sumCredit
        else:
            # even
            total = sumCredit - sumDebit
            
        #print "%s Debit: %f Credit: %f %d %s" % (self.name, sumDebit, sumCredit, self.type, self.type & 1)

        return total