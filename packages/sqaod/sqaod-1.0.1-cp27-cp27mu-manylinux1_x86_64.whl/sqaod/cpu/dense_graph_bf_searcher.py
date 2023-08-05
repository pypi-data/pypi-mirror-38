from __future__ import print_function
import numpy as np
import sqaod
from sqaod.common.dense_graph_bf_searcher_base import DenseGraphBFSearcherBase
from . import cpu_dg_bf_searcher as cext

class DenseGraphBFSearcher(DenseGraphBFSearcherBase) :

    def __init__(self, W, optimize, dtype, prefdict) :
        self._cobj = cext.new(dtype)
        DenseGraphBFSearcherBase.__init__(self, cext, dtype, W, optimize, prefdict)


def dense_graph_bf_searcher(W = None, optimize = sqaod.minimize, dtype=np.float64, **prefs) :
    """ factory function for sqaod.cpu.DenseGraphAnnealer.

    Args:
      numpy.ndarray : QUBO
      optimize : specify optimize direction, `sqaod.maximize or sqaod.minimize <preference.html#sqaod-maximize-sqaod-minimize>`_.
      prefs : `preference <preference.html>`_ as \*\*kwargs
    Returns:
      sqaod.cpu.DenseGraphBFSearcher: brute-force searcher instance
    """
    
    return DenseGraphBFSearcher(W, optimize, dtype, prefs)


if __name__ == '__main__' :

    np.random.seed(0)
    dtype = np.float32
    N = 8
    W = np.array([[-32,4,4,4,4,4,4,4],
                  [4,-32,4,4,4,4,4,4],
                  [4,4,-32,4,4,4,4,4],
                  [4,4,4,-32,4,4,4,4],
                  [4,4,4,4,-32,4,4,4],
                  [4,4,4,4,4,-32,4,4],
                  [4,4,4,4,4,4,-32,4],
                  [4,4,4,4,4,4,4,-32]])

    N = 16
    W = sqaod.generate_random_symmetric_W(N, -0.5, 0.5, dtype);
    bf = dense_graph_bf_searcher(W, sqaod.minimize, dtype)
    bf.set_preferences(tile_size=256)
    
    import time

    start = time.time()
    bf.search()
    end = time.time()
    print(end - start)
    
    x = bf.get_x() 
    E = bf.get_E()
    print(E)
    print(x)
    print(bf.get_preferences())
    
#    import sqaod.py.formulas
#    E = np.empty((1), dtype)
#    for bits in x :
#        print sqaod.py.formulas.dense_graph_calculate_E(W, bits)
