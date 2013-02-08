'''
Created on Dec 19, 2012

@author: thospy
'''
import unittest
import os

from libs import Database
#from accounts import Account
from tenants import *
from products import *
#from sqlalchemy.sql import func

class ProductsTest(unittest.TestCase):

    def setUp(self):
        dbFile = "/tmp/testing_products.db"
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

    def test_createProduct(self):
        product2 = Product(name="USB Hub", number="ABC-1235", price=32.60, description="Blubb")
        product2.save()
        
        ## Way 1 to add a new document
        document = Document(type=Document.BILL, partner=Partner(name="Customer GmbH"))
        document.save()
        
        documentposition1 = Documentposition(document_id=document.id, product=Product(name="USB Stick", number="ABC-1234", price=12.50, description="Blubb"), deduction=0.0, quantity=2)
        documentposition1.save()
        documentposition2 = Documentposition(document_id=document.id, product=product2, deduction=0.0, quantity=3)
        documentposition2.save()
        docsum = document.sum()
        self.assertAlmostEqual(first=docsum, second=122.8, msg="There is a wrong price %f not equal to %f" % (docsum, float(122.80)))

        ## Way 2 to add a new document
        docs = [
            Documentposition(product=Product(name="Harddisk", number="ABC-1236", price=129.90, description="Blubb"), deduction=10, quantity=1),
            Documentposition(product=product2, deduction=0.0, quantity=1)
        ]

        document2 = Document(documentpositions=docs, type=Document.BILL, partner=Partner(name="Customer2 GmbH"))
        document2.save()
        docsum = document2.sum()
        self.assertEqual(str(document2.esr()), "0100000149510>000000000000000000000000026+ 010045167>", "ESR line does not match")
        self.assertAlmostEqual(first=docsum, second=149.51, msg="There is a wrong price %f not equal to %f" % (docsum,float(149.51)))
        
        print document.serialize()['Document']

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()