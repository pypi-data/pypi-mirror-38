#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*FACADE PATTER - What is this pattern about?
The Facade pattern is a way to provide a simpler unified interface to
a more complex system. It provides an easier way to access functions
of the underlying system by providing a single entry point.
This kind of abstraction is seen in many real life situations. For
example, we can turn on a computer by just pressing a button, but in
fact there are many procedures and operations done when that happens
(e.g., loading programs from disk to memory). In this case, the button
serves as an unified interface to all the underlying procedures to
turn on a computer.

*What does this example do?
The code defines three classes (QC1, QC2, QC3) that represent complex
parts to be tested. Instead of testing each class separately, the
TestRunner class acts as the facade to run all tests with only one
call to the method runAll. By doing that, the client part only needs
to instantiate the class TestRunner and call the runAll method.
As seen in the example, the interface provided by the Facade pattern
is independent from the underlying implementation. Since the client
just calls the runAll method, we can modify the classes QC1, QC2 or
QC3 without impact on the way the client uses the system.

*Where is the pattern used practically?
This pattern can be seen in the Python standard library when we use
the isdir function. Although a user simply uses this function to know
whether a path refers to a directory, the system makes a few
operations and calls other modules (e.g., os.stat) to give the result.

*References:
https://sourcemaking.com/design_patterns/facade
https://fkromer.github.io/python-pattern-references/design/#facade
http://python-3-patterns-idioms-test.readthedocs.io/en/latest/ChangeInterface.html#facade

Provides a simpler unified interface to a complex system.
"""

from __future__ import print_function
import time
from manual_decline.arpsfcn import arpsfcn
SLEEP = 0.1


# Complex Parts
class QClassOne:
    def run(self):
        print(u"###### In Test 1 ######")
        time.sleep(SLEEP)
        print(u"Setting up")
        time.sleep(SLEEP)
        print(u"Running test")
        time.sleep(SLEEP)
        print(u"Tearing down")
        time.sleep(SLEEP)
        print(u"Test Finished\n")

    def qclassone_fun(self):
        print('i was called as qclassone_fun')
        return 'ok'

class QClassTwo:
    def run(self):
        print(u"###### In Test 2 ######")
        time.sleep(SLEEP)
        print(u"Setting up")
        time.sleep(SLEEP)
        print(u"Running test")
        time.sleep(SLEEP)
        print(u"Tearing down")
        time.sleep(SLEEP)
        print(u"Test Finished\n")


class QClassThree:
    def run(self):
        print(u"###### In Test 3 ######")
        time.sleep(SLEEP)
        print(u"Setting up")
        time.sleep(SLEEP)
        print(u"Running test")
        time.sleep(SLEEP)
        print(u"Tearing down")
        time.sleep(SLEEP)
        print(u"Test Finished\n")

class FitArps:


    def __init__(self,buildupMonths = 0, buildupRate = 0,q1 = 0,b1=0,d1=0,t1=0,q2=0,b2=0,d2=0,t2=0,dMin = 0.05,phase="",id="",_startDate = None,_refDate = None, _offset = 0, _cumul = 0.0 ):
        print("initializing")
        self.buildupMonths = buildupMonths
        self.buildupRate = buildupRate

        self.q1= q1
        self.b1 = b1
        self.d1 = d1
        self.t1 = t1
        self.q2 = q2
        self.b2 = b2
        self.d2 = d2
        self.t2 = t2
        self.dMin = dMin
        self._startDate = _startDate
        self._refDate = _refDate
        self.phase = phase
        self.id = id
        self._offset = _offset
        self._cumul = _cumul

    def __str__(self):

        return str(self.__dict__)

    def getRates(self, t):
            #leg 0
            arps = arpsfcn()
            arps.generateRates(self.buildupRate, 0.0,0.0,0.0, self.buildupMonths)
            eur = arps.getDouble("eur")
            rates0 = arps.getArray("rates")
            #leg 1
            arps = arpsfcn()
            arps.generateRates(self.q1, self.b1, self.d1, self.dMin, int(self.t1))
            eur += arps.getDouble("eur")
            rates1 = arps.getArray("rates")

            #leg 2
            arps = arpsfcn()
            arps.generateRates(self.q2,self.b2,self.d2,self.dMin, min(t - int(self.t1) - int(self.buildupMonths), int(self.t2)))
            eur += arps.getDouble("eur")
            rates2 = arps.getArray("rates")

            #stitch the arrays together
            #nMos = len(rates0) + len(rates1) + len(rates2)
            rates = []
            #cums = []
            #cumul = 0.0
            idx = 0
            idx2 = len(rates1)
            idx3 = len(rates0) + len(rates1)
            for i in range(0,len(rates0)):
                rates.insert(idx,rates0[i])
                idx += 1
            for i in range(0, len(rates1)):
                rates.insert(idx2, rates1[0])
                idx2 += 1
            for i in range(0,len(rates2)):
                rates.insert(idx3, rates2[0])
                idx3 += 1
            return rates

    def getEURWithOffsetVariableFrame(self,t):
            #init
            cumul = 0.0

            #calculate the rates
            rates = self.getRates(t + self._offset)
            nMos = len(rates)
            cums = [0]
            print(' got here getEUR')
            #Accumulate the entire stream
            for i in range(self._offset, nMos - 1):
                cums.insert(i,cums[i] + rates[i] * 30.4167)
                cumul += cums[i]
            return cumul

# Facade Patterns
class QRunner:

    def __init__(self):

        self.qc2 = QClassTwo()
        self.qc3 = QClassThree()
        self.tests = [self.qc2, self.qc3]

    def runAll(self):
        [i.run() for i in self.tests]

    def run_fit_arps(self,**kwargs):
        fitarps =FitArps(**kwargs)

        print(f'{fitarps}')#(buildupMonths = 25, buildupRate = 964.15,q1 = 1807.77,b1=2.00,d1=0.49,t1=0.0,q2=1807.77,b2=1.14,d2=0.56,t2=575.0,dMin = 0.05,phase="Gas",id="238",_startDate = None,_refDate = None)}')
        print(f'and eUR={fitarps.getEURWithOffsetVariableFrame(4)}')

# Client
if __name__ == '__main__':
    qrunner = QRunner()
    qrunner.runAll()
    reqParams ={'buildupMonths' : 25, 'buildupRate' : 964.15,'q1' : 1807.77,'b1':2.00,'d1':0.49,'t1':0.0,'q2':1807.77,'b2':1.14,'d2':0.56,'t2':575.0,'dMin' : 0.05,'phase':"Gas",'id':"238",'_startDate': None,'_refDate' : None}
    qrunner.run_fit_arps(**reqParams)

### OUTPUT ###
