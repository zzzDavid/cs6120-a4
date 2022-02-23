# CS6120 Advanced Compiler
## Assignment 4 Dataflow Solver

This repository is an implementation of the worklist algorithm
as a general dataflow sovler. It supports five passes:
- Reaching definitions
- Live variables
- Constant propagation
- Available expressions → common sub-expression elimination
- Constant folding

All tests in `df` can be checked with `turnt ./df/*.bril`

## Run
### Reaching Definition
```
❯ bril2json < df/cond.bril | python main.py -reach
```
### Live variables
```
❯ bril2json < df/cond.bril | python main.py -live
```
### Constant propagation 
```
❯ bril2json < df/idchain-nonlocal.bril | python main.py -const_prop | python dce.py -g | bril2txt
```
### Common Sub-expression Elimination
```
❯ bril2json < df/cse-nonlocal.bril | python main.py -cse | bril2txt
```
### Constant Folding
```
❯ bril2json < df/cse-nonlocal.bril | python main.py -cf | bril2txt
```

## Test
Run any test in the `df` folder with turnt:
```
❯ turnt ./df/*.bril
```
