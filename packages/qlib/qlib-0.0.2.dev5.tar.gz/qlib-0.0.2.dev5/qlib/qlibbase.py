class QLibBase():
   
    version=''

    def  __init__(self,ver='0.0.1'):
        self.version = ver

    def doSay(self,message="Called from QLibBase"):
        return f"{message} @version={self.version}"

        


