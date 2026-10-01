import unittest
import numpy as np
import pandas as pd
from scripts.predictor_ablation import new_predictors
class AblationTest(unittest.TestCase):
    def test_weighted_absolute_not_mean_delta(self):
        means={('A','p'):np.array([5.,10.]),('A','control'):np.array([1.,1.]),
               ('B','p'):np.array([20.,30.]),('B','control'):np.array([4.,5.]),('T','control'):np.array([3.,4.])}
        counts={('A','p'):1,('B','p'):3}
        keys=pd.DataFrame([{'outSample':'T','perturb':'p'}])
        z=new_predictors(keys,means,counts,['g1','g2'])
        np.testing.assert_array_equal(z['analytic_trainMean'][0]['delta'],[13.25,21.])
        np.testing.assert_array_equal(z['meanDelta'][0]['delta'],[10.,17.])
    def test_missing_control_refused(self):
        with self.assertRaises(ValueError):
            new_predictors(pd.DataFrame([{'outSample':'T','perturb':'p'}]),
                {('A','p'):np.array([1.,2.]),('T','control'):np.array([0.,0.])},{('A','p'):1},['g1','g2'])
if __name__=='__main__':unittest.main()
