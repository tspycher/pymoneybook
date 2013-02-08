'''
Created on Dec 18, 2012

@author: thospy


'''
import unittest
import os

from libs import Database
from accounts import * 
from tenants import *
from products import *


class AccountsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dbFile = "/tmp/testing_accounts.db"
        if os.path.exists(dbFile):
            os.unlink(dbFile)
        db = Database.instance('sqlite:///%s' % dbFile)
        db.buildTables()
        
        # Create Tenant
        tenant = Tenant(name="zerodine GmbH", esr_account="01-1234-5", esr_reference_prefix="999888")
        tenant.save()
        Current.instance(id=tenant.id)

    def tearDown(self):
        pass
    
    def test_accountImport(self):
        Account.importAccounts(os.path.abspath("../import/accounts/kmu/active-accounts.csv"), Account.ACTIVE)
        Account.importAccounts(os.path.abspath("../import/accounts/kmu/passive-accounts.csv"), Account.PASSIVE)
        Account.importAccounts(os.path.abspath("../import/accounts/kmu/income-accounts.csv"), Account.INCOME)
        Account.importAccounts(os.path.abspath("../import/accounts/kmu/expense-accounts.csv"), Account.EXPENSE)
        import json
        print json.dumps(Account.accountList(Account.ACTIVE), indent=1)
        print json.dumps(Account.accountList(Account.PASSIVE), indent=1)
        print json.dumps(Account.accountList(Account.INCOME), indent=1)
        print json.dumps(Account.accountList(Account.EXPENSE), indent=1)

    def test_createAccount(self):
        accountActive = Account(name="Bank",number="1100",type=Account.ACTIVE)
        accountActive.save()
        accountAufwand = Account(name="Aufwand1",number="3100",type=Account.AUFWAND)
        accountAufwand.save()
        accountErtrag = Account(name="Ertrag1",number="4100",type=Account.ERTRAG)
        accountErtrag.save()
        accountKreditor = Account(name="Kreditor1",number="2200",type=Account.PASSIVE)
        accountKreditor.save()
        self.assertIsNotNone(accountActive, "Could not create Account, is None")
        
        accountAny = Account(name="Any",number="4100",type=Account.ERTRAG)
        accountAny.save()
        accountAny.bookSoll(2000.0, accountAny)

        soll = 1000.0
        haben = 400.0
        
        accountActive.bookSoll(soll, accountErtrag)
        accountActive.bookHaben(haben, accountAufwand)
        
        rechnung = 150.0
        accountKreditor.bookHaben(rechnung, accountAufwand, "Bestellung auf Rechnung")
        accountActive.bookHaben(rechnung, accountKreditor, "Bezahlung der Rechung")

        self.assertEqual(accountErtrag.saldo(), soll, "The Saldo of the Account is not equal %f" % (soll))
        self.assertEqual(accountAufwand.saldo(), haben+rechnung, "The Saldo of the Account is not equal %f" % (haben+rechnung))
        self.assertEqual(accountActive.saldo(), soll-haben-rechnung, "The Saldo of the Account is not equal %f" % (soll-haben-rechnung))

    def test_document_accounting(self):
        docs = [
            Documentposition(product=Product(name="Harddisk", number="ABC-1236", price=129.90, description="Blubb"), deduction=10, quantity=1),
            Documentposition(product=Product(name="Cable", number="ABC-1237", price=11.10, description="A cool cable"), deduction=0.0, quantity=1)
        ]

        document2 = Document(documentpositions=docs, type=Document.BILL, partner=Partner(name="Customer2 GmbH"))
        document2.save()
        
        Account(name="Debitor1",number="1201",type=Account.ACTIVE).save()
        Account(name="Verkauf von Hardware",number="4101",type=Account.INCOME).save()
        Account(name="New Bank",number="1101",type=Account.ACTIVE).save()
        
        document2.bookInvoiceSend(Account.byNumber("1201"),Account.byNumber("4101"))
        self.assertEqual(document2.sum(), Account.byNumber("1201").saldo(), "Debitor Saldo is not equal")
        self.assertEqual(document2.sum(), Account.byNumber("4101").saldo(), "Income Saldo is not equal")

        document2.bookInvoicePaid(Account.byNumber("1201"), Account.byNumber("1101"))
        self.assertEqual(document2.sum(), Account.byNumber("4101").saldo(), "Income Saldo is not equal")
        self.assertEqual(Account.byNumber("1201").saldo(), 0.0 , "Debitor Saldo is not 0.0")
        self.assertEqual(document2.sum(), Account.byNumber("1101").saldo(), "Bank Saldo is not equal")
        
        #print document2.jsonSerialize()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()