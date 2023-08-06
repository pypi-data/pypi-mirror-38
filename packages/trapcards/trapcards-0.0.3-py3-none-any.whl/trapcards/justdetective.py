import re

class JustDetective:    
    ## undefined value detector
    @staticmethod
    def simpleDetect(value):
        if (value != '' and value != None and value != [] ):
            return True
        else:
            return False
    
    @staticmethod
    def isMatchRegex(string, reg):
        return bool(re.match(reg, str(string)))