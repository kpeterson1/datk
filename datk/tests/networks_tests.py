"""
Network Test Suite

Tests Netwoks defined in networks.py by visual inspection
"""

try:
    from datk.core.networks import *
    from datk.core.tester import Tester
except ImportError:
    raise ImportError(
""" Imports failed\n
To run tests, execute the following commands:
$ cd ../..
$ python -m datk.tests.networks_tests """)

try:
    __IPYTHON__
    ip = get_ipython()
    ip.magic("%matplotlib inline") 
except NameError:
    pass

tester = Tester(DEFAULT_TIMEOUT = 10, TEST_BY_DEFAULT = True, MAIN_THREAD_BY_DEFAULT = True)
test=tester.test

@test
def DRAW_RANDOM():
    Random_Line_Network(25).draw()

@test
def DRAW_HUGE_RANDOM():
    Random_Line_Network(100, sparsity=0.2).draw()

@test
def DRAW_UNI_RING():
    Unidirectional_Ring(4).draw()

@test
def DRAW_BI_RING():
    Bidirectional_Ring(7).draw()

@test
def DRAW_COMPLETE_GRAPH():
    Complete_Graph(10).draw()

@test
def DRAW_UNI_LINE():
    Unidirectional_Line(4).draw()

@test
def DRAW_BI_LINE():
    Bidirectional_Line(5).draw()

tester.summarize()