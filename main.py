import json
import copy
import sys

from basic_block import form_basic_blocks
from control_flow_graph import *

def worklist(cfg):
    """The worklist algorithm
    - cfg: a dictionary of blocks
    """
    def merge(ins):
        """
        - ins: a list of sets
        - return: a set
        """
        res = set()
        for i in ins:
            res = res.union(i)
        return res

    def transfer(bb, ins):
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

    # ins and outs are dicts: {str : set()}
    # initialize
    ins = dict()
    outs = dict()
    for label, _ in cfg.items():
        ins[label] = set()
        outs[label] = set()
    worklist = copy.deepcopy(cfg)
    while len(worklist) > 0:
        # pick any block from worklist
        # I'll just pick the first one
        label = list(worklist.keys())[0]
        bb = worklist.pop(label)
        bb_ins = [outs[label] for label in bb.pred]
        bb_ins_merged = merge(bb_ins)
        ins[label] = bb_ins_merged
        bb_outs  = transfer(bb, bb_ins_merged)
        if len(bb_outs) != outs[label]:
            outs[label] = bb_outs
            for succ in bb.succ:
                worklist[succ] = cfg[succ]
    print(ins)
    print(outs)

def main():
    # read from file because it's easier to debug this way
    with open(sys.argv[1], "r") as infile:
        prog = json.load(infile)

    # prog = json.load(sys.stdin)
    for func in prog['functions']:
        blocks = form_basic_blocks(func['instrs'])
        blocks = [b for b in blocks if len(b) > 0]
        cfg = CFG(blocks).cfg
        worklist(cfg)

if __name__ == "__main__":
    main()