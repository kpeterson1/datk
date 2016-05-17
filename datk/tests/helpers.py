"""
Helper functions for tests in tests.py
"""
from datk.core.distalgs import Process
import sys
from datk.core.helpers import *

def assertLeaderElection(
    network,
    isLeader = lambda p: "status" in p.state and p.state["status"]=="leader",
    isNonleader = lambda p: "status" in p.state and p.state["status"]=="non-leader"
    ):
    """Asserts that exactly one Process is Leader, and all other processes are Non-Leader"""

    assert sum([isLeader(p) for p in network]) == 1 , "Leader Election Failed"
    assert sum([isNonleader(p) for p in network]) == len(network)-1, "Leader Election Failed"

def assertBroadcast(network, attr):
    """Asserts that p.state[attr] is identical for all processes p"""
    for p in network:
        assert attr in p.state
    assert len(set([p.state[attr] for p in network])) == 1, "Broadcasting " + attr + " failed."

def assertBFS(network):
    """Asserts that every Process, p, knows 'parent', and there 
     exists exactly one Process where 'parent' is None"""
    found_root = False
    for p in network:
        assert 'parent' in p.state, "BFS Failed. state['parent'] not found."
        if p.state['parent'] is None:
            if found_root:
                assert False, "BFS failed. No unique root node"
            else:
                found_root = True
        else:
            assert isinstance(p.state['parent'], Process), "BFS FAILED"

def assertBFSWithChildren(network):
    """Asserts that every Process, p, knows 'parent' and 'children', and there
    exists exactly one Process where 'parent' is None"""
    found_root = False
    for p in network:
        assert 'parent' in p.state, "BFS Failed. state['parent'] not found."
        if p.state['parent'] is None:
            if found_root:
                assert False, "BFS failed. No unique root node"
            else:
                found_root = True
        else:
            assert isinstance(p.state['parent'], Process), "BFS FAILED"
            assert p in p.state['parent'].state['children'], "BFS FAILED"

def assertLubyMIS(network):
    """Asserts that every process knows a boolean value, 'MIS', and that the Processes
    where 'MIS' is True form a set that is both independent and maximal."""
    for process in network:
        assert 'MIS' in process.state, "'MIS' not in Process state"
        assert isinstance(process.state['MIS'], bool)
        if process.state['MIS'] == True:
            assert not any([nbr.state['MIS'] for nbr in process.out_nbrs]), 'MIS not independent'
        if process.state['MIS'] == False:
            assert any([nbr.state['MIS'] for nbr in process.out_nbrs]), 'MIS not maximal'

# helpers for consensus algorithms, e.g. FloodSet
def assertConsensus(network):
    """Asserts that every Process, p, that has not failed decides upon the same 'decision' value by the termination of the algorithm, 
    and that the final value decided upon is not 'failed'"""
    num_p_failed = 0
    decision = 'no decision'
    for p in network:
        assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.\n")
        if p.state['decision'] is "failed":
            num_p_failed += 1
        else:
            if decision is 'no decision':
                decision = p.state['decision']
            else:
                assert 'decision' in p.state, print_error("Consensus Failed. state['decision'] not found.\n")
                assert p.state['decision'] == decision and decision != "failed", print_error("Consensus Failed. Agreement not reached among all processes.\n")

    hasDecided = lambda p: "decision" in p.state and p.state["decision"] == decision
    total_p = len([p for p in network])
    assert sum([hasDecided(p) for p in network]) == (total_p - num_p_failed) , print_error("Consensus Failed. \n")

def assertConsensusWithValueInInitialSet(network, algorithm):
    """Asserts that every Process, p, that has not failed decides upon the same 'decision' value, and that the final
     value decided upon exists in V, the initial set of possible decision values from which a process could choose as its 'decision'"""
    num_p_failed = 0
    decision = 'no decision'
    initial_V = algorithm.params["V"] # returns a set of the initial input values
    for p in network:
        assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.\n")
        if p.state['decision'] is "failed":
            num_p_failed += 1
        else:
            if decision is 'no decision':
                decision = p.state['decision']
            else:
                assert 'decision' in p.state, print_error("Consensus Failed. state['decision'] not found.\n")
                assert decision in initial_V,  print_error("Process reached consensus on value: " + decision + " but this value is not in the initial set of input values, V: " + str(initial_V))
                assert p.state['decision'] == decision, print_error("Consensus Failed. Agreement not reached among all processes.\n")

    hasDecided = lambda p: "decision" in p.state and p.state["decision"] == decision
    total_p = len([p for p in network])
    assert sum([hasDecided(p) for p in network]) == (total_p - num_p_failed) , print_error("Consensus Failed. \n")
    if decision is not 'no decision':
        # need a way to set V in example network 
        assert True, print_error("Consensus Failed. Final decision value not in initial set of possible decision values \n")
        assert decision in initial_V,  print_error("Process reached consensus on value: " + decision + " but this value is not in the initial set of input values, V: " + str(initial_V))

def assertNoConsensus(network):
    """Asserts that no consensus is reached, meaning that every Process, p, that has not failed does not agree upon
    the same, single value. No consensus will also be reached if every process fails.
     """
    num_p_failed = 0
    decision = 'no decision'
    for p in network:
        assert 'decision' in p.state, print_error("state['decision'] not found.")
        if p.state['decision'] is "failed":
            num_p_failed += 1
        else:
            if decision is 'no decision':
                decision = p.state['decision']
            else:
                assert 'decision' in p.state, print_error("state['decision'] not found.\n")
                assert p.state['decision'] == decision and decision == "failed" , print_error("Consensus Succeeded.\n EXPECTED: not all processes reached same decision.\n ACTUAL: All processed agreed on some value.\n \
                    However, this error may not be problematic, if running a test when only some processes should fail. Try increasing the value of the parameter 'failure_prob' so that more processes fail.\n")


def assertConsensusOnDefaultValue(network):
    """Asserts that every Process, p, that has not failed decides upon the same 'decision' value, and that the final
     value decided upon is v_0, the specified default value.
     """
    # test case where all processes startwith initial values = v_0
    # TODO : fill in test

def assertConsensusOnInitialValue(network, algorithm):
    """Asserts that every Process, p, that has not failed decides upon the same 'decision' value, and that the final
     value decided upon is v_0, the specified default value. This test assumes that all processes start with the same value, v_0.
     """
    # test case where all processes start with initial values = v_0
    v_0 = algorithm.params["v_0"]
    V = algorithm.params["V"]
    for p in network:
        assert 'decision' in p.state, print_error("state['decision'] not found.\n")
        assert v_0 in V, print_error("The initial value " + str(v_0) + "was not found in the initial set of input values, " + str(V))
        assert p.state['decision'] == v_0, print_error("EXPECTED: process's decision = " + str(v_0) + ".\n ACTUAL: process's decision = " + str(p.state['decision']))


def assertSomeFail(network, algorithm):
    """Asserts that if one or more of the Processes, p, has failed, but the total number of failed processes is less than f, the total allowed number
    of failures, then consensus is still reached. Alternatively, if the total number of failed processes exceeds f, then the algorithm fails and consensus is NOT reached.
     """
    num_p_failed = 0
    decision = 'no decision'
    for p in network:
        assert 'decision' in p.state, print_error("state['decision'] not found.\n")
        if p.state['decision'] is "failed":
            num_p_failed += 1
        else:
            if decision is 'no decision':
                decision = p.state['decision']
            else:
                assert 'decision' in p.state, print_error("state['decision'] not found.\n")
                if algorithm.params["f"] >= num_p_failed >= 1:
                    assert p.state['decision'] == decision and decision == "failed" , print_error("Consensus Succeeded.\n EXPECTED: not all processes reached same decision.\n ACTUAL: All processed agreed on some value.\n")
                else:
                    assert p.state['decision'] == decision and decision != "failed", print_error("Consensus Failed. Agreement not reached among all processes.\n")

def assertOneFailsNoConsensusInRing(network):
    """Given a Uni-Ring or Bi-Ring network, asserts that if one or more of the Processes, p, has failed during execution of the
    algorithm, consensus is not reached.
     """
    num_p_failed = 0
    total_p = len([p for p in network])
    decision = 'no decision'
    for p in network:
        assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.")
        if p.state['decision'] is "failed":
            num_p_failed += 1
        else:
            if decision is 'no decision':
                decision = p.state['decision']
    if num_p_failed >= 1:
        assert p.state['decision'] == decision and decision == "failed" , print_error("Consensus Succeeded.\n EXPECTED: some processes have the decision 'failed.'\n ACTUAL: All processes agreed on some value that is not 'failed'.\n")


def assertOneFailsAllFailInRing(network):
    """Given a Uni-Ring or Bi-Ring network, asserts that if one or more of the Processes, p, has failed during execution of the
    algorithm, all processes have the decision state set to 'failed' by the termination of the algorithm, and the algorithm fails (i.e.
    no consensus reached).
     """
    num_p_failed = 0
    total_p = len([p for p in network])
    decision = 'no decision'
    for p in network:
        assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.")
        if p.state['decision'] is "failed":
            num_p_failed += 1
        else:
            if decision is 'no decision':
                decision = p.state['decision']
    if num_p_failed >= 1:
        assert num_p_failed == total_p , print_error("Floodset Failed. Not all processes failed as expected.\n EXPECTED: " + str(total_p) + "/" + str(total_p) + " failed.\n ACTUAL: "+ str(num_p_failed) + "/" + str(total_p) + " failed. \n")

def assertAllFailed(network):
    """Asserts that every Process, p, has failed by the termination of the algorithm
     """
    num_p_failed = 0
    total_p = len([p for p in network])
    for p in network:
        assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.")
        if p.state['decision'] is "failed":
            num_p_failed += 1
    assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.")
    assert num_p_failed == total_p , print_error("Floodset Failed. Not all processes failed as expected.\n EXPECTED: " + str(total_p) + "/" + str(total_p) + " failed.\n ACTUAL: "+ str(num_p_failed) + "/" + str(total_p) + " failed. \n")

def assertAllAlive(network):
    """Asserts that every Process, p, remains alive and has NOT failed by the termination of the algorithm
     """
    num_p_failed = 0
    total_p = len([p for p in network])
    for p in network:
        assert p.state['decision'] != "unknown", print_error("Floodset Failed. state['decision'] not found.")
        if p.state['decision'] is "failed":
            num_p_failed += 1
    assert 'decision' in p.state, print_error("Floodset Failed. state['decision'] not found.")
    assert num_p_failed != total_p , print_error("Floodset Failed. Not all processes survived as expected; some have failed.")
    assert num_p_failed == 0, print_error("Floodset Failed. Not all processes survived as expected; some have failed.\n EXPECTED: " + str(total_p) + "/" + str(total_p) + " survived.\n ACTUAL: "+ str(total_p - num_p_failed) + "/" + str(total_p) + " survived. \n")


