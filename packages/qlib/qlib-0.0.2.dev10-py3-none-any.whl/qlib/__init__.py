#__version__ = "0.0.2dev"
name="qlib"
import qlib.qlibbase
from qlib.qlibbase import QLibBase
import qlib.manual_decline.fitarps
from qlib.manual_decline.fitarps import FITArps

def testclass():
    qtool = QLibBase()
    dosay = qtool.doSay()
    return dosay
def testfit():
    
    arps = FITArps()    