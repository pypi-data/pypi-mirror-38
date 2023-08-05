# SBBClassifier
VX: Python implementation of **Symbiotic Bid-Based (SBB)** framework for problem decomposition using Genetic Programming (GP). Algorithm developed by the NIMS laboratory, Dalhousie University, Canada. This implementation can be used as a library to apply GP to classification tasks.

## 1. References
**PhD Thesis**

Lichodzijewski, P. (2011) A Symbiotic Bid-Based (SBB) framework for problem decomposition using Genetic Programming, PhD Thesis ([link](http://web.cs.dal.ca/~mheywood/Thesis/PLichodzijewski.pdf))

## 2. How to Run

To run this algorithm in Python:
```
from vx.SBB.sbb import SBB
from vx.SBB.config import Config

if __name__ == "__main__":
    Config.check_parameters()
    SBB().run()
```

All configurable options are in the SBB/config.py file, in the variable CONFIG.
