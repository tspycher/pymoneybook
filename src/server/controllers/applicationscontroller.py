import tornado.web
import json
import re

class ApplicationsController(tornado.web.RequestHandler):
    action = "index"
    method = "get"
    urlData = []
    data = None
    isJson = False
    
    def initialize(self):
        pass
    
    def get(self, *args, **kwargs):
        """
        Handels get HTTP Requests
        """
        self._callAction(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.method = "post"
        if self.request.body: 
            try:
                self.data = json.loads(str(self.request.body))
                self.isJson = True
            except ValueError:
                #print "Post Data is not Json String"
                self.data = str(self.request.body)
        self._callAction(*args, **kwargs)
    
    def _callAction(self, *args, **kwargs):
        self.urlData = []
        m = re.search('[^/]*', str(args[0]))
        if str(m.group(0)): self.action = str(m.group(0))
        if not self.action in dir(self):
            self.set_status(404)
            self.write_error(404)
            return
        for x in str(args[0]).split('/')[1:]: self.urlData.append(x)
        #print self.urlData
        getattr(self, self.action)(**kwargs)
    
    def writeJson(self,data):
        self.clear()
        #self.add_header("Content-Type", "application/json")
        try:
            self.write(data)
        except:
            #print "Could not respond as json"
            self.set_status(500)
            self.write_error(500)
        #self.finish()
    
    def present500(self, message = None):
        self.set_status(500)
        self.write_error(500)
        self.logger.log.error(message)
        

