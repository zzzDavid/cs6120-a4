from distutils.command.build_clib import build_clib
import json
import copy
import sys

from basic_block import form_basic_blocks

TERMINATORS = ['jmp', 'ret', 'br']

class BasicBlock(object):
    def __init__(self, block):
        self.instrs = block
        self.pred = []
        self.succ = []

class CFG(object):
    """
    Give each block succ and pred 
    """
    def __init__(self, blocks, reverse=False):
        self.blocks = blocks
        self.cfg = dict()
        self.reverse = reverse
        self.build_cfg()
    
    def build_cfg(self):
        # convert blocks from a list to a dictionary
        for block in self.blocks:
            # go through all blocks
            # build a list of Blocks
            bb = BasicBlock(block)
            label = "start"
            if "label" in block[0]:
                label = block[0]['label']
            self.cfg[label] = bb

        # add succ and pred to the basic blocks
        for label, bb in self.cfg.items():
            # check the ternimator instr
            op = bb.instrs[-1]['op']
            if op not in TERMINATORS: continue
            if op == "jmp":
                jmp_target = bb.instrs[-1]['labels'][0]
                self.cfg[label].succ.append(jmp_target)
                self.cfg[label].pred.append(label)
            elif op == "br":
                br_targets = bb.instrs[-1]['labels']
                for target in br_targets:
                    self.cfg[label].succ.append(target)
                    self.cfg[target].pred.append(label)

def remove_from_set(in_set, dest):
    out_set = set()
    for i in in_set:
        if 'dest' not in i: continue
        if dest != i['dest']: out_set.add(i)
    return out_set

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
            res.union(i)
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
        bb_ins = [ins[label] for label in bb.pred]
        bb_ins_merged = merge(bb_ins)
        ins[label] = bb_ins_merged
        bb_outs  = transfer(bb, bb_ins_merged)
        if len(bb_outs) != outs[label]:
            outs[label] = bb_outs
            for succ in bb.succ:
                worklist[succ] = cfg[succ]
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