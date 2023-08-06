# Copyright 2018 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Real hafnian function
========================

**Module name:** :mod:`hafnian.rlhaf`

.. currentmodule:: hafnian.rlhaf

Summary
--------

.. autosummary::
    hafnian

Code details
-------------
"""
import ctypes
import os
import numpy as np


path = os.path.dirname(__file__)
sofile = os.path.join(path, "lib/rlhafnian.so")
cdll = ctypes.CDLL(sofile)


_calc_hafnian = cdll.dhaf
_calc_hafnian.restype = ctypes.c_double

_calc_hafnian_loops = cdll.dhaf_loops
_calc_hafnian_loops.restype = ctypes.c_double


def hafnian(l, loop=False):
    """Returns the hafnian of real matrix l via the C hafnian library.

    Args:
        l (array): a real, square, symmetric array of even dimensions.
        loop (bool): If ``True``, the loop hafnian is returned. Default false.

    Returns:
        np.float64: the hafnian of matrix l
    """
    if l.dtype != np.float64:
        l = l.astype(np.float64)
    matshape = l.shape
    a = l.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    rr = np.float64(np.array([0.0, 0.0]))
    arr = rr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    if loop:
        res = _calc_hafnian_loops(a, matshape[0], arr) # pylint: disable=unused-variable
    else:
        res = _calc_hafnian(a, matshape[0], arr) # pylint: disable=unused-variable

    return rr[0]
