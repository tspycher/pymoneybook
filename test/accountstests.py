'''
Created on Dec 18, 2012

@author: thospy


'''
import unittest
import os

from libs import Database
from accounts import Account 

class AccountsTest(unittest.TestCase):


    def setUp(self):
        dbFile = "/tmp/testing_accounts.db"
        if os.path.exists(dbFile):
            os.unlink(dbFile)

        db = Database.instance('sqlite:///%s' % dbFile)
        db.buildTables()


    def tearDown(self):
        pass


    def test_createAccount(self):
        accountActive = Account(name="Bank",number="1100",type=Account.ACTIVE)
        accountActive.save()
        accountAufwand = Account(name="Aufwand1",number="3100",type=Account.AUFWAND)
        accountAufwand.save()
        accountErtrag = Account(name="Ertrag1",number="4100",type=Account.ERTRAG)
        accountErtrag.save()
        self.assertIsNotNone(accountActive, "Could not create Account, is None")
        
        accountAny = Account(name="Any",number="4100",type=Account.ERTRAG)
        accountAny.save()
        accountAny.bookSoll(2000, accountAny)

        soll = 1000
        haben = 400
        
        accountActive.bookSoll(soll, accountErtrag)
        accountActive.bookHaben(haben, accountAufwand)
        
        self.assertEqual(accountActive.saldo(), soll-haben, "The Saldo of the Account is not equal %d" % (soll-haben))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()