'''
Created on Dec 18, 2012

@author: thospy


'''
import unittest
import os

from libs import Database
from accounts import * 
from tenants import *


class AccountsTest(unittest.TestCase):


    def setUp(self):
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
        accountAny.bookSoll(2000.0, accountAny)
        accountAny.save()

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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()