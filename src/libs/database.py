'''
Created on Oct 10, 2012

@author: thospy
'''


import datetime
import json

try:
    from sqlalchemy import create_engine #, ForeignKey
    #from sqlalchemy import Column, Date, Integer, String
    from sqlalchemy.ext.declarative import declarative_base 
    #from sqlalchemy.orm import relationship, backref
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Column, DateTime, Integer, String
except ImportError:
    import sys
    sys.stderr.write("Looks like you do not have SQLAlchemy installed (apt-get install python-sqlalchemy)")
    sys.exit(1)

from libs import Singleton, Logger

Base = declarative_base()

@Singleton
class Database(object):
    '''
    The DB Class should only exits once, thats why it has the @Singleton decorator.
    To Create an instance you have to use the instance method:
        db = Database.instance()
    '''
    engine = None
    session = None
    
    def __init__(self, dburi):
        if not self.engine and not self.session:
            Logger.instance().log.info("Connecting to db %s" % dburi)
            self.engine = create_engine(dburi, echo=False)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
    
    def buildTables(self):
        ## Create all Tables
        Base.metadata.create_all(self.engine)
    
    def instance(self, *args, **kwargs):
        '''
        dummy function to prevent any IDE of showing an syntax error
        '''
        pass

class BaseModel(object):
    '''
    This is a baseclass with delivers all basic database operations
    '''
    
    created = Column(DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)
    updated = Column(DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)
    
    logger = Logger.instance()
    
    def save(self, commit = True):
        db = Database.instance()
        db.session.add(self)
        if commit: db.session.commit()
    
    def saveMultiple(self, objects = [], commit = True):
        db = Database.instance()
        db.session.add_all(objects)
        if commit: db.session.commit()
        
    def update(self, commit = True):
        db = Database.instance()
        if commit: db.session.commit()
    
    def delete(self, commit = True):
        db = Database.instance()
        db.session.delete(self)
        if commit: db.session.commit()
        
    def queryObject(self):
        db = Database.instance()
        return db.session.query(self.__class__)
    
    def serialize(self):
        data = {}
        data[self.name()] = {}
        
        for x in list(self.__class__.__dict__):
            if x[0] != "_":
                attr = getattr(self, x)
                
                if(attr.__class__.__name__ == "datetime"):
                    attr = attr.strftime("%d/%m/%Y %H:%M:%S")
                if(attr.__class__.__name__ == "instancemethod"):
                    attr = "method"
                if issubclass(attr.__class__, Base):
                    #attr = attr.serialize()
                    #attr = "OBJECT"
                    continue
                if(attr.__class__.__name__ == "InstrumentedList"):
                    newAttr = []
                    for y in attr:
                        if hasattr(y, "serialize") and callable(getattr(y, "serialize")):
                            newAttr.append(y.serialize())
                        else:
                            newAttr.append(y.__class__.__name__)
                    attr = newAttr
                
                #attr = attr.__class__.__name__
                data[self.name()][x] = attr
        return data
    
    def jsonSerialize(self):
        data = self.serialize()
        return json.dumps(data,indent=4)
    
    def name(self):
        return str(self.__class__.__name__).replace("Model", "")
        
    #def __repr__(self):
        #return "<%s(%s)>" % (self.name(), self.serialize())
