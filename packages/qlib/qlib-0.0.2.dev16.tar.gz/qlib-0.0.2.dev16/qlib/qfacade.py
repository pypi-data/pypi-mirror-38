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
from .manual_decline.arpsfcn import arpsfcn
from .manual_decline.thbfcn import thbfcn
from .manual_decline.fitarps import fitarps
from .manual_decline.fitthb import fitthb
from .manual_decline.thb2arps import thb2arps

# Complex and inherited from manual decline
''' keep adding classes to be in sync with Brennan changes...
    Pattern is good when we need to change the inner then client use
    wont need to know...
'''
# Facade Patterns
class QFacade(object):

    def __init__(self):

        self.fitarps = fitarps
        self.thbfcn = thbfcn
        self.fitthb = fitthb
        self.arpsfcn = arpsfcn



    def run_fit_arps(self,**kwargs):
        fitarpsObj = self.fitarps
        return fitarpsObj


    def run_thb_fcn(self,**kwargs):
        thbfcnObj = self.thbfcn
        return thbfcnObj

    def run_fit_thb(self,**kwargs):
        fitthbObj = self.fitthb
        return fitthbObj

    def run_arps_fcn(self,**kwargs):
        arpsObj = self.arpsfcn
        return arpsObj

    def run_thb2_arps(self, **kwargs):
        thb2arpsObj = thb2arps
        return thb2arpsObj


# Client
if __name__ == '__main__':
    qrunner = QFacade()
    #qrunner.runAll()
    reqParams ={'buildupMonths' : 25, 'buildupRate' : 964.15,'q1' : 1807.77,'b1':2.00,'d1':0.49,'t1':0.0,'q2':1807.77,'b2':1.14,'d2':0.56,'t2':575.0,'dMin' : 0.05,'phase':"Gas",'id':"238",'_startDate': None,'_refDate' : None}
    qrunner.run_fit_arps(**reqParams)
    #test run fit_fnc classs
    qi = 966
    di = 0.65
    bf = 1.2
    telf = 0.0
    dMin = 0.05
    fcmons = 600
    timedata = []
    for i in range(0,fcmons):
	    timedata.insert(i,(30.4167 * i))
    #thb = thbfcn([],[],0.0,0.0)
    reqParam2={'rates' : [] , 'bAvg' :[] , 'cumul': 0.0, 'eurProxy': 0.0}
    qrunner.run_thb_fcn(**reqParam2)
    #thb.generateRatesTHB(qi,2,bf,di,telf,dMin,timedata)

### OUTPUT ###
