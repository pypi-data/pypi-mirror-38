#__version__ = "0.0.2dev"
name="qlib"
import qlib.qlibbase
from qlib.qlibbase import QLibBase, QApi
from qlib.qfacade import QFacade
import qlib.manual_decline
from qlib.manual_decline.arpsfcn import arpsfcn
#import qlib.manual_decline.fitarps
#from qlib.manual_decline.fitarps import FITArps
#from qlib.manual_decline.arps import *
#from qlib.manual_decline.fitarps import fitarps
#from fitarps import getEURWithOffsetVariableFrame

def testclass():
    qtool = QLibBase()
    dosay = qtool.doSay()
    return dosay
'''def testfit():
    print('i called fitarps')
    fit=fitarps(buildupMonths = 25, buildupRate = 964.15,q1 = 1807.77,b1=2.00,d1=0.49,t1=0.0,q2=1807.77,b2=1.14,d2=0.56,t2=575.0,dMin = 0.05,phase="Gas",id="238",_startDate = None,_refDate = None)
	#print(f'{fitarps.getEURWithOffsetVariableFrame(2)}')
    #arps = fitarps()
    print(fit.getEURWithOffsetVariableFrame(2))
'''
def test_qapi(username,password):
    print('i called test_aqpi')
    qapi= QApi('http://localhost:5000/qapi_login')
    token=qapi.apilogin(username,password)
    return token
def test_get_resource(url,headers):
    pass
if __name__=='__main__':
    #testfit()
    token=test_qapi('sub1','test11')
    if not token:
        print('see fail message')
    print(token)
