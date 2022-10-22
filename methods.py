class Trace(object):
    def __init__(self,env):
        self.env = env       
    def registerrequest(self):
        	yield self.env.timeout(2400)       
    def examinecasually(self):
        	yield self.env.timeout(5280)       
    def checkticket(self):
        	yield self.env.timeout(578640)       
    def decide(self):
        	yield self.env.timeout(10800)       
    def reinitiaterequest(self):
        	yield self.env.timeout(252900)       
    def examinethoroughly(self):
        	yield self.env.timeout(167820)       
    def paycompensation(self):
        	yield self.env.timeout(264660)       
    def rejectrequest(self):
        	yield self.env.timeout(244934)       
    