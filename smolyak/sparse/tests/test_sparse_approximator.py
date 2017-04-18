'''
Test smolyak.sparse.sparse_approximator
'''
import unittest
from smolyak.sparse.sparse_approximator import SparseApproximator 
from smolyak.misc.snooze import snooze
import numpy as np
import cProfile
import pstats


class TestSparseApproximator(unittest.TestCase):
    
    def setUp(self):
        """init each test"""
        self.pr = cProfile.Profile()
        self.pr.enable()
        print "\n<<<---"
        
    def tearDown(self):
        """finish any test"""
        p = pstats.Stats(self.pr)
        p.strip_dirs()
        # p.sort_stats ('cumtime')
        # p.print_stats ()
        p.sort_stats('cumulative').print_stats(20)
        print "\n--->>>"
    
    def test_dimensionadaptivity(self):
        ndim = 5
        def decomposition(i):
            ii = [v for __, v in i.sparse_tuple()]
            value = np.exp(-sum(ii))
            return value + snooze(2 ** sum(ii))
        SA = SparseApproximator(decomposition=decomposition, init_dims=1,
                           next_dims=lambda dim: [dim + 1] if dim < ndim - 1 else [])
        SA.expand_adaptive(c_steps=50)
        self.assertAlmostEqual(SA.get_contribution_exponent(0), 1, delta=0.1)
        
    def test_bundled(self):
        bundled = [0, 1]
        def decomposition(mis):
            value = sum([np.exp(-3 * mi[0]) * np.exp(-mi[1]) * np.exp(-mi[2]) for mi in mis])
            return value + snooze(2 ** mi[0] * 2 ** mi[1] * 2 ** mi[2])
        SA = SparseApproximator(decomposition=decomposition, init_dims=3, is_bundled=bundled,
                                work_factor=[np.log(2), np.log(2), np.log(2)], contribution_factor=[3, 1, 1])
        SA.expand_nonadaptive(L=15, c_dim=3)
        T = SA.get_approximation()
        self.assertAlmostEqual(T, 1 / (1 - np.exp(-3)) * 1 / (1 - np.exp(-1)) * 1 / (1 - np.exp(-1)), places=2, msg='Limit incorrect')

    def test_notbundled(self):
        def decomposition(i):
            value = 3.**(-i[0]) * 5.**(-2 * i[1]) * 7.**(-3 * i[2])
            return value + snooze(2 ** i[0] * 2 ** i[1] * 2 ** i[2])
        contribution_factor = lambda i: 3.**(-float(i[0])) * 5.**(-2 * float(i[1])) * 7.**(-3 * float(i[2]))
        SA = SparseApproximator(decomposition, init_dims=3,
                                contribution_factor=contribution_factor)
        SA.expand_adaptive(c_steps=75, T_max=2)
        self.assertAlmostEqual(SA.get_approximation(), 3. / 2 * 25. / 24 * 343. / 342, places=2)
        self.assertAlmostEqual(SA.get_work_exponent(0), np.log(2), delta=0.2)
        self.assertAlmostEqual(SA.get_work_exponent(2), np.log(2), delta=0.2)
        
    def test_notbundled2(self):
        def decomposition(i):
            value = 3.**(-i[0]) * 5.**(-2 * i[1]) * 7.**(-3 * i[2])
            return value + snooze(2 ** i[0] * 2 ** i[1] * 2 ** i[2])
        SA = SparseApproximator(decomposition, init_dims=3)
        SA.continuation(L_max=20)
        self.assertAlmostEqual(SA.get_approximation(), 3. / 2 * 25. / 24 * 343. / 342, places=3)
        self.assertAlmostEqual(SA.get_work_exponent(0), np.log(2), delta=0.2)
        self.assertAlmostEqual(SA.get_work_exponent(2), np.log(2), delta=0.2)
        self.assertAlmostEqual(SA.get_contribution_exponent(0), np.log(3), delta=0.2)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
