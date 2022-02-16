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
                self.cfg[jmp_target].pred.append(label)
            elif op == "br":
                br_targets = bb.instrs[-1]['labels']
                for target in br_targets:
                    self.cfg[label].succ.append(target)
                    self.cfg[target].pred.append(label)