import unittest
import pandas as pd
from itertools import combinations
from selective_transfer.selector_utility import utility
from selective_transfer.evaluation import CLEAN_DATASETS
class UtilityTest(unittest.TestCase):
    def setUp(self):
        self.m=pd.DataFrame([dict(dataset=ds,context='ctx',perturbation=str(i),pcc_delta=.2+.1*i,mse=.01,certificate=i)
                             for ds in CLEAN_DATASETS for i in range(5)])
        self.b=self.m[['dataset','context','perturbation','pcc_delta']].copy()
    def test_expected_uniform_random_and_identical_masks(self):
        t,c,u,v=utility(self.m,self.b)
        self.assertAlmostEqual(t.iloc[0].random_expected_method_risk,
                               sum(sum(1-self.m.iloc[i].pcc_delta for i in ix)/4 for ix in combinations(range(5),4))/5)
        self.assertAlmostEqual(t.iloc[0].retained_method_risk,t.iloc[0].matched_mask_baseline_risk)
        self.assertFalse(v['clause_A_pass']);self.assertTrue(v['clause_B_pass'])
    def test_nonidentifiable(self):
        t,c,u,v=utility(self.m[self.m.perturbation!='4'],self.b[self.b.perturbation!='4'])
        self.assertFalse(t.selector_identifiable.any());self.assertFalse(v['clause_A_pass'])
    def test_key_mismatch_refused(self):
        with self.assertRaises(ValueError):utility(self.m,self.b.iloc[1:])
    def test_order_invariant(self):
        a=utility(self.m,self.b)[3];b=utility(self.m.sample(frac=1,random_state=1),self.b.sample(frac=1,random_state=2))[3]
        self.assertAlmostEqual(a['retained_macro_method_risk'],b['retained_macro_method_risk'])
if __name__=='__main__':unittest.main()
