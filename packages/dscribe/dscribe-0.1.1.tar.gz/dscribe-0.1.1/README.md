```text
     _                _ _
    | |              (_) |
  __| | ___  ___  ___ _| |__   ___
 / _` |/ __|/ __| '__| | '_ \ / _ \
| (_| |\__ \ (__| |  | | |_) |  __/
 \__,_||___/\___|_|  |_|_.__/ \___|
```

[![Build Status](https://travis-ci.org/SINGROUP/dscribe.svg?branch=master)](https://travis-ci.org/SINGROUP/dscribe)
[![Coverage Status](https://coveralls.io/repos/github/SINGROUP/dscribe/badge.svg?branch=master)](https://coveralls.io/github/SINGROUP/dscribe?branch=master)

dscribe is a python package for creating machine learning descriptors for atomistic systems.

# Example
```python
from dscribe.descriptors import MBTR
from dscribe.descriptors import CoulombMatrix
from dscribe.descriptors import SineMatrix
import dscribe.utils

import ase.io

#===============================================================================
# 1. DEFINING AN ATOMISTIC SYSTEM
#===============================================================================
# Load configuration from an XYZ file with ASE. See
atoms = ase.io.read("nacl.xyz")
atoms.set_cell([5.640200, 5.640200, 5.640200])
atoms.set_initial_charges(atoms.get_atomic_numbers())

#===============================================================================
# 2. CREATING DESCRIPTORS FOR THE SYSTEM
#===============================================================================
# Getting some basic statistics from the processed systems. This information is
# used by the different descriptors for e.g. zero padding.
stats = dscribe.utils.system_stats([atoms])
n_atoms_max = stats["n_atoms_max"]
min_distance = stats["min_distance"]
atomic_numbers = stats["atomic_numbers"]

# Defining the properties of the descriptors
cm_desc = CoulombMatrix(n_atoms_max=n_atoms_max, permutation="sorted_l2")
sm_desc = SineMatrix(n_atoms_max=n_atoms_max)
mbtr_desc = MBTR(
    atomic_numbers=atomic_numbers,
    k=[1, 2],
    grid={
        "k1": {"min": 11, "max": 17, "sigma": 0.1, "n": 50},
        "k2": {"min": 0, "max": 1/min_distance, "sigma": 0.01, "n": 50}
    },
    periodic=True,
    weighting={
        "k2": {
            "function": "exponential",
            "scale": 0.5,
            "cutoff": 1e-3
        }
    }
)

# Creating the descriptors
cm = cm_desc.create(atoms)
sm = sm_desc.create(atoms)
mbtr = mbtr_desc.create(atoms)

# When dealing with multiple systems, create the descriptors in a loop. This
# allows you to control the final output format and also allows you to create
# multiple descriptors from the same system, while using cached intermediate
# results to speed up calculation.
ase_atoms = ase.io.iread("multiple.extxyz", format="extxyz")
for atoms in ase_atoms:
    atoms.set_initial_charges(atoms.get_atomic_numbers())
    cm = cm_desc.create(atoms)
    sm = sm_desc.create(atoms)
    mbtr = mbtr_desc.create(atoms)

#===============================================================================
# 3. USING DESCRIPTORS IN MACHINE LEARNING
#===============================================================================
# The result of the .create() function is a (possibly sparse) 1D vector that
# can now be directly used in various machine-learning libraries.
```

# Installation
To install the package, clone the repository and install with pip, e.g.

```sh
git clone https://github.com/SINGROUP/dscribe.git
cd dscribe
pip install .
```
