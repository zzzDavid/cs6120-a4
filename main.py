import json
import sys

from basic_block import form_basic_blocks




def main():
    # read from file because it's easier to debug this way
    with open(sys.argv[1], "r") as infile:
        prog = json.load(infile)

    # prog = json.load(sys.stdin)
    
    for func in prog['functions']:
        blocks = form_basic_blocks(func['instrs'])
        for block in blocks:
            print(block)


if __name__ == "__main__":
    main()