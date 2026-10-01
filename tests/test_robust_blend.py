import unittest
import numpy as np
from selective_transfer.robust_blend import WEIGHTS,select_blend,components
from selective_transfer.core import ridge_corrected_transfer
class BlendTest(unittest.TestCase):
    def test_grid(self):
        self.assertEqual(len(WEIGHTS),15)
        self.assertTrue(all(sum(w)==1 and min(w)>=0 for w in WEIGHTS))
    def test_fallback_exact_ridge(self):
        d=np.array([[1.,2.,4.],[3.,2.,5.]]);c=np.array([[1.,1.,3.],[4.,2.,3.]])
        n=np.array([4,9]);t=np.array([2.,3.,4.])
        p,r=select_blend(d,c,n,t)
        np.testing.assert_array_equal(p,ridge_corrected_transfer(d,c,t,n).predicted_delta)
        self.assertTrue(r['fallback'])
    def test_tie_lexicographic_and_constant_inner(self):
        d=np.ones((3,4));c=np.zeros((3,4));n=np.ones(3,dtype=int)
        p,r=select_blend(d,c,n,np.zeros(4))
        self.assertEqual(r['weights'],[0.,0.,1.]);self.assertEqual(r['worst_training_pcc'],-1.)
    def test_target_control_never_selects_weights(self):
        d=np.array([[1.,2.,4.,6.],[3.,1.,5.,8.],[2.,4.,3.,7.]])
        c=np.array([[1.,1.,3.,4.],[4.,2.,3.,1.],[1.,3.,2.,5.]])
        n=np.array([4,9,7])
        a=select_blend(d,c,n,np.zeros(4))[1];b=select_blend(d,c,n,np.ones(4)*100)[1]
        self.assertEqual(a,b)
if __name__=='__main__':unittest.main()
