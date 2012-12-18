"""
.. module:: incamail
   :synopsis: Configuration Factory, Singleton
.. moduleauthor:: Thomas Spycher <thomas.spyche@tech.swisssign.com>
"""
import ConfigParser
import os
from libs import Singleton
import cStringIO

#from sws.cloud import Endpointmanager

@Singleton
class Configuration(object):
    '''
    This class helps to handle all settings for the whole application. It has been implemented as an singleton
    cause of any module in the lib folder can and many do use their own configuration settings.
    
    Its hard do pass the path of the configuration file trough the whole call stack to any module. The executeable
    file in sbin creats the first instance of the this class and passes the path to the configuration file to it. Every
    calles sub library gets a copy of the same instance without piping the path of the config file to it.
    
    So every module has access to the same configfile.
    The Singleton has been implemented in :mod:singleton
    '''
    _config = None #: The instance of ConfigParser
    _defaultConfig = None
    _configFile = None #: Configuration Filename
    _defaultFilename = "pyncacore.conf"
    
    def __init__(self,configFile = None):
        '''
        Constructor which creates an instance of ConfigParser
        
        :param configFile: The absolute path to the configfile
        :type configFile: str
        ''' 
        if not configFile:
            configFile = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../etc/%s' % self._defaultFilename))
        
        #self._verifyConfigFile(configFile)
        if not self._config:
            self._configFile = configFile
            self._config = ConfigParser.RawConfigParser()
            self._config.read(configFile)
            
            # The _defaultConfig is used to track all configuration parameters for creating
            # complete configuration files
            self._defaultConfig = ConfigParser.ConfigParser()
    
    def configFile(self):
        return self._configFile
    
    def _verifyConfigFile(self, configFile):
        try:
            open(configFile, "r")
        except Exception:
            raise MissingConfigFileException(configFile)
        else:
            return True
        
    def get(self, section, option, default = None):
        ''' Reads an setting from the config file and if not present returns the default value instad of throwing an
        exeception.
        
        :param section: the section [section] name in the configfile
        :param option: the name of the option in the section
        :param default: default value which gets returned if option has not been found
        '''
        #print "Configfile: %s Section: %s Option: %s" % (self._configFile, section, option)
        
        try:
            self._defaultConfig.add_section(section)
            self._defaultConfig.set(section, option, default)
        except ConfigParser.DuplicateSectionError:
            pass
        
        if not self._config.has_section(section) or not self._config.has_option(section, option):
            return default
        return self._config.get(section, option)

    def instance(self, *args, **kwargs):
        '''
        dummy function to prevent any IDE of showing an syntax error
        '''
        pass
    
    def getDefaultConfig(self):
        '''Writes the default config to an Buffered String for returning it 
        as an string
        '''
        defaultConfig =  cStringIO.StringIO()
        self._defaultConfig.write(defaultConfig)
        data = defaultConfig.getvalue()
        defaultConfig.close()
        return str(data)
    
    '''def endpointCallback(self, addr, message):
        #print "Message %s from %s" % (message,addr)
        em = Endpointmanager(self.get('cloud','endpointfile', '/tmp/endpoints.config'))
        em.cleanStaleEndpoints()
        em.addEndpoint(message['service'], addr[0])
        #em.addEndpoint(message['service'], addr[0])
    
    def getRandomEndpoint(self, service):
        em = Endpointmanager(self.get('cloud','endpointfile', '/tmp/endpoints.config'))
        return em.giveEndpoint(endpointtype=service, randomEndpoint=True)
        
        '''

class MissingConfigFileException(Exception):
    def __init__(self, confiFile):
        self.value = confiFile

    def __str__(self):
        return repr("Could not read the configfile %s" % self.value)