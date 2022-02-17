import copy

from tomlkit import value 
from lvn import *
# Reaching Definitions

def merge_reaching(ins):
    """
    - ins: a list of sets
    - return: a set
    """
    res = set()
    for i in ins:
        res = res.union(i)
    return res

def transfer_reaching(bb, ins):
    """ Transfer function for live variables: DEF U (IN - KILL)
    - bb: BasicBlock
    - ins: a set of str
    - return: a set of str
    """
    defs = set()
    reaching_vars = copy.deepcopy(ins)
    for instr in bb.instrs:
        if 'dest' not in instr: continue
        if instr['dest'] in ins:
            # we just killed a variable
            # removed it from ins
            reaching_vars.remove(instr['dest'])
        else: # we add a new definition
            defs.add(instr['dest'])
    return defs.union(reaching_vars)

# Constant Propagation
def merge_lvn(ins):
    """
    - ins: a list of sets
    - return: a set
    """
    res = set()
    for i in ins:
        res = res.union(i)
    return res

def transfer_lvn(bb, ins):
    """
    - bb: BasicBlock
    - ins: a set of value tuple
    - return: a set of value tuple
    """
    """
    My idea of implementing constant propagation
    and other lvn-related stuff is to generate
    value tuples at the input of each basic block
    """
    # Do const folding, const propagation
    instrs = lvn(bb.instrs, ins, False)
    # replace basic block's old instructions with optimized ones
    bb.instrs = instrs
    res = copy.deepcopy(ins)
    for instr in instrs:
        # skip the labels
        if 'dest' not in instr: continue
        if 'op' not in instr: continue
        # Build value tuple
        if 'args' in instr:
            value_tuple = (instr['dest'], instr['op'], *instr['args'])
        else: # const instr
            value_tuple = (instr['dest'], instr['op'], instr['value'])
        res.add(value_tuple)
    return res

def transfer_cf(bb, ins):
    """
    - bb: BasicBlock
    - ins: a set of value tuple
    - return: a set of value tuple
    """
    """
    My idea of implementing constant propagation
    and other lvn-related stuff is to generate
    value tuples at the input of each basic block
    """
    # Do const folding, const propagation
    instrs = lvn(bb.instrs, ins, True)
    # replace basic block's old instructions with optimized ones
    bb.instrs = instrs
    res = copy.deepcopy(ins)
    for instr in instrs:
        # skip the labels
        if 'dest' not in instr: continue
        if 'op' not in instr: continue
        # Build value tuple
        if 'args' in instr:
            value_tuple = (instr['dest'], instr['op'], *instr['args'])
        else: # const instr
            value_tuple = (instr['dest'], instr['op'], instr['value'])
        res.add(value_tuple)
    return res

# Live variables
def merge_live(ins):
    res = set()
    for i in ins:
        res = res.union(i)
    return res

def transfer_live(bb, ins):
    alive = copy.deepcopy(ins)
    reversed_instrs = copy.deepcopy(bb.instrs)
    reversed_instrs.reverse()
    for instr in reversed_instrs:
        if 'dest' in instr and instr['dest'] in alive:
            # we just found a necessary variable
            # that is defined here
            # so we remove it from alive_vars
            # we just killed a variable
            alive.remove(instr['dest'])
        # the args needs to be added to "alive_vars"
        if 'args' in instr:
            for arg in instr['args']:
                alive.add(arg)
    return alive