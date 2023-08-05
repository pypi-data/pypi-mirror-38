#__version__ = "0.0.2dev"
name="qlib"
import qlib.qlibbase
from qlib.qlibbase import QLibBase

def testclass():
    qtool = QLibBase()
    dosay = qtool.doSay()
    return dosay