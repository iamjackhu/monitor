import telnetlib
import os
from ConfigParser import SafeConfigParser
from monitor.service.singleton import SingletonMixin
from monitor.service.config import ConfigManager

class SwitchDetector(SingletonMixin):

    def __init__(self):
        self.config = ConfigManager.instance().getConfig()
        self.telnetip = self.config.get("switch", "telnetip")
        self.username = self.config.get("switch", "username")
        self.password = self.config.get("switch", "password")
        self.portStatus = {}

    def getSwitchIP(self):
        return self.telnetip

    def pullStatus(self):

        portStatus = {}

        tn = telnetlib.Telnet(self.telnetip)
        tn.read_until("User Access Verification")
        tn.write("%s\n"%self.username)
        tn.read_until("Password:")
        tn.write("%s\n"%self.password)
        tn.write("enable\n")
        tn.read_until("Password:")
        tn.write("%s\n"%self.password)
        tn.write("show interfaces status\n")
        tn.write("    ")
        tn.write("\n")
        tn.write("exit\n")

        result = tn.read_all()

        # print result
        lines = result.split("\n")
        for line in lines:
            words = line.split()
            if(len(words) > 3):
                if(words[2] in ("up","down","Unknown")):
                    portStatus['%s'%(words[1])] = words[2]
                # print "%s-%s : %s " % (words[0][0], words[1], words[2])

        # print portStatus
        tn.close()

        return portStatus

    def getStatus(self):
        return NotImplemented

if __name__ == '__main__':
    switcher = SwitchDetector()
    switcher.pullStatus()
