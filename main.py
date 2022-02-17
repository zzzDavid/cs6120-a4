import argparse
import json
import copy
import sys

from basic_block import form_basic_blocks
from control_flow_graph import *
from merge_transfer_funcs import *
from printer import *

def worklist(cfg, merge_func, transfer_func, printer):
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
        if len(bb_outs) != len(outs[label]):
            outs[label] = bb_outs
            for succ in bb.succ:
                worklist[succ] = cfg[succ]
    
    if printer is not None:
        printer(ins, outs)
    

def main(reach, live, const_prop, cse, file=None):
    # read from file because it's easier to debug this way
    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)

    # prog = json.load(sys.stdin)

    if reach:
        reverse = False
        printer = Printer(reverse=False)
        merge_fn = merge_reaching
        transfer_fn = transfer_reaching
    elif live:
        reverse = True
        printer = Printer(reverse=True)
        merge_fn = merge_live
        transfer_fn = transfer_live
    elif const_prop:
        reverse = False 
        printer = None
        merge_fn = merge_lvn
        transfer_fn = transfer_lvn
    elif cse:
        reverse = False
        printer = None
    else:
        raise Exception("invalid input choice argument")

    for func in prog['functions']:
        blocks = form_basic_blocks(func['instrs'])
        blocks = [b for b in blocks if len(b) > 0]
        control_flow_graph = CFG(blocks, reverse=reverse)
        cfg = control_flow_graph.cfg
        worklist(cfg, merge_fn, transfer_fn, printer)
        func['instrs'] = control_flow_graph.gen_instrs()
    
    if const_prop or cse: 
        print(json.dumps(prog, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-reach', dest='reach_definitions',
                        default=False, action='store_true',
                        help='reach definitions')
    parser.add_argument('-live', dest='live_variable',
                        default=False, action='store_true',
                        help='live_variable')
    parser.add_argument('-const_prop', dest='const_prop',
                        default=False, action='store_true',
                        help='Constant propagation')
    parser.add_argument('-cse', dest='cse',
                        default=False, action='store_true',
                        help='CSE')
    parser.add_argument('-f', dest='filename', 
                        action='store', type=str, help='json file')
    args = parser.parse_args()
    reach = args.reach_definitions
    live = args.live_variable
    const_prop = args.const_prop
    cse = args.cse
    file = args.filename
    main(reach, live, const_prop, cse, file)