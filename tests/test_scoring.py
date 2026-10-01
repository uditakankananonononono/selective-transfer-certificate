import unittest
import numpy as np
import pandas as pd
from selective_transfer.scoring import selected_mean,assert_exact_keys
class Fake:
    n_vars=3
    X=np.array([[1.,2.,3.],[3.,4.,9.],[999.,999.,999.]])
class ScoreTest(unittest.TestCase):
    def test_all_cells_exact_mean(self):
        np.testing.assert_array_equal(selected_mean(Fake(),np.array([0,1]),1),[2,3,6])
    def test_missing_unit_refused(self):
        r=pd.DataFrame([{'dataset':'A','context':'B','perturbation':str(i)} for i in range(2)])
        with self.assertRaises(ValueError):assert_exact_keys(r.iloc[:1],r)
    def test_duplicate_unit_refused(self):
        r=pd.DataFrame([{'dataset':'A','context':'B','perturbation':'p'}])
        with self.assertRaises(ValueError):assert_exact_keys(pd.concat([r,r]),r)
if __name__=='__main__':unittest.main()
