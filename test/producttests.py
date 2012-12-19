'''
Created on Dec 19, 2012

@author: thospy
'''
import unittest
import os

from libs import Database
#from accounts import Account 
from products import *

class ProductsTest(unittest.TestCase):


    def setUp(self):
        dbFile = "/tmp/testing_accounts.db"
        if os.path.exists(dbFile):
            os.unlink(dbFile)
        db = Database.instance('sqlite:///%s' % dbFile)
        db.buildTables()


    def tearDown(self):
        pass


    def test_createProduct(self):
        product1 = Product(name="USB Stick", number="ABC-1234", price=12.50, description="Blubb")
        product1.save()
        product2 = Product(name="USB Hub", number="ABC-1235", price=32.60, description="Blubb")
        product2.save()
        
        document = Document(type=Document.BILL, customer=Customer(name="Customer GmbH"))
        document.save()
        
        documentposition1 = Documentposition(document_id=document.id, product_id=product1.id, deduction=0.0, quantity=2)
        documentposition1.save()
        
        self.assertEqual(document.sum(), product1.price*2, "There is a wrong price %f" % product1.price*2)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()