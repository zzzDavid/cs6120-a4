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
    alive_vars = [i['dest'] for i in ins if 'dest' in i] 
    for instr in bb.instrs:
        if 'dest' not in instr: continue
        if instr['dest'] in alive_vars:
            # we just killed a variable
            # removed it from ins
            # ins = remove_from_set(ins, instr['dest'])
            ins.remove(instr['dest'])
        else: # we add a new definition
            defs.add(instr['dest'])
    return defs.union(ins)
