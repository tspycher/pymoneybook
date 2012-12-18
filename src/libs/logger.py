'''
Created on Nov 1, 2012

@author: thospy
'''
from libs import Singleton, Configuration
import logging


@Singleton
class Logger(object):
    
    log = None
    
    def __init__(self):
        conf = Configuration.instance()
        
        if not self.log:
            self.log = logging.getLogger('pymoneybook')
            self.log.setLevel(logging.DEBUG)
            
            # create file handler which logs even debug messages
            fh = logging.FileHandler(conf.get('Logging', 'logfile', '/tmp/pymoneybook.log'))
            fh.setLevel(logging.DEBUG)
            
            # create console handler with a higher log level
            ch = logging.StreamHandler()
            #ch.setLevel(logging.ERROR)
            ch.setLevel(logging.DEBUG)
            
            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - (%(levelname)s) %(name)s/%(module)s - %(message)s')
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            
            # add the handlers to logger
            self.log.addHandler(ch)
            self.log.addHandler(fh)
    
    @staticmethod
    def instance(*args, **kwargs):
        '''
        dummy function to prevent any IDE of showing an syntax error
        '''
        pass