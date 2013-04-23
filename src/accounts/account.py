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
from tenants import currentTenant

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey, event
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
    parent_id = Column(Integer,ForeignKey("accounts.id"))

    name = Column(String, unique=False)
    number = Column(Integer)
    type = Column(Integer)
    
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant",backref=backref("accounts", order_by=id))
    
    
    def bookSoll(self, amount, otherAccount, text = None, document=None):
        return self.bookDebit(amount, otherAccount, text, document)
    
    def bookDebit(self, amount, otherAccount, text = None, document=None):
        return self._book(self, otherAccount, amount, text, document)
    
    def bookHaben(self,amount, otherAccount, text = None, document=None):
        return self.bookCredit(amount, otherAccount, text, document)
        
    def bookCredit(self, amount, otherAccount, text = None, document=None):
        return self._book(otherAccount, self, amount, text, document)
    
    def _book(self, debitAccount, creditAccount, amount, text,document=None):
        return Journal(accountDebit_id=debitAccount.id, accountCredit_id=creditAccount.id, amount=amount, text=text,document_id=document).save()
    
    @staticmethod
    def importAccounts(filename, typeofAccount):
        import csv
        f = open(filename, 'rb')
        r = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in r:
            parent = None
            if row['parent']:
                parent = Account.byNumber(row['parent']).id
                #parent = row['parent']
            
            a = Account(number=row['number'], parent_id=parent, name=unicode(row['name']),type=typeofAccount, tenant_id=currentTenant())
            a.save()
            if row['start']:
                pass
                #Journal(accountDebit_id=a.id, amount=row['start'], text="Saldo from Import").save()
        f.close()
        
    @staticmethod
    def accountList(accountType = 1):
        accounts = []
        a = Account().queryObject().filter(Account.type == accountType,Account.parent_id == None, Account.tenant_id == currentTenant()).all()
        for account in a:
            x = {"id":account.id, "number":account.number, "name":account.name}
            parents = Account._iter(account)
            if parents:
                x["parents"] = parents
            accounts.append(x)
        return {"accounts":accounts}
    
    @staticmethod
    def _iter(account):
        accounts = []
        a = Account().queryObject().filter(Account.parent_id == account.id).all()
        if not a:
            return
        
        for account in a:
            x = {"id":account.id, "number":account.number, "name":account.name}
            parents = Account._iter(account)
            if parents:
                x["parents"] = parents
            accounts.append(x)
        return accounts
    
    @staticmethod
    def byNumber(number):
        return Account().queryObject().filter(Account.number==number).first()
        
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

event.listen(Account, 'before_insert', Account.gen_tenant_id)
event.listen(Account, 'before_update', Account.gen_tenant_id)