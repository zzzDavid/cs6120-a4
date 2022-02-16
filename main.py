import json
import copy
import sys

from basic_block import form_basic_blocks
from control_flow_graph import *
from merge_transfer_funcs import *

def worklist(cfg, merge_func, transfer_func):
    """The worklist algorithm
    - cfg: a dictionary of blocks
    """
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
        bb_ins_merged = merge_func(bb_ins)
        ins[label] = bb_ins_merged
        bb_outs  = transfer_func(bb, bb_ins_merged)
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
        # cfg = CFG(blocks).cfg
        # worklist(cfg, merge_reaching, transfer_reaching)
        cfg = CFG(blocks, reverse=True).cfg
        worklist(cfg, merge_live, transfer_live)

if __name__ == "__main__":
    main()