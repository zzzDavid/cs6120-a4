
def print_set(s):
    if len(s) == 0:
        print("∅")
    else:
        for i, v in enumerate(list(s)):
            if i == len(s) - 1:
                print(v)
            else:
                print(v, end=', ')

class Printer(object):
    def __init__(self, reverse=False) -> None:
        self.reverse = reverse
    def __call__(self, ins, outs):
        for key in ins.keys():
            print(f"{key}:")
            if self.reverse:
                print("  in:\t", end='')
                print_set(outs[key])
                print("  out:\t", end='')
                print_set(ins[key])
            else:
                print("  in:\t", end='')
                print_set(ins[key])
                print("  out:\t", end='')
                print_set(outs[key])