import copy 
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