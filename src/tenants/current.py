'''
Created on Feb 8, 2013

@author: thospy
'''
from libs import Singleton
from tenant import Tenant

class NoTenantError(Exception):
    pass

@Singleton
class Current(object):
    tenant = None
    
    def __init__(self, name = None, id = None):
        if name:
            # Searching for Tenant by name
            self.tenant = Tenant().queryObject().filter(Tenant.name==name).first()
        else:
            # Searching for Tenant by id
            self.tenant = Tenant().queryObject().filter(Tenant.id==id).first()
        
        if not self.tenant:
            raise NoTenantError


def currentTenant():
    try:
        return int(Current.instance().tenant.id)
    except:
        return 1