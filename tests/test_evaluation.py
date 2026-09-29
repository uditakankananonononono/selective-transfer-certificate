import unittest
import numpy as np
import pandas as pd
from selective_transfer.evaluation import assess,CLEAN_DATASETS

class EvaluationTest(unittest.TestCase):
    def setUp(self):
        self.targets=pd.DataFrame([{'dataset':ds,'pcc_delta':.5} for ds in CLEAN_DATASETS])
        self.rows=pd.DataFrame([{'dataset':ds,'context':'ctx','perturbation':str(i),
                                 'pcc_delta':.6,'mse':.05,'certificate':float(i)}
                                for ds in CLEAN_DATASETS for i in range(4)])

    def test_small_sets_actual_coverage_and_win(self):
        table,verdict=assess(self.rows,self.targets)
        self.assertTrue((table.actual_coverage==1).all())
        self.assertAlmostEqual(verdict['relative_risk_reduction'],.2)
        self.assertTrue(verdict['overall_win'])

    def test_exact_five_abstains_one(self):
        more=pd.DataFrame([{'dataset':ds,'context':'ctx','perturbation':'extra',
                            'pcc_delta':-.9,'mse':.2,'certificate':-1.}
                           for ds in CLEAN_DATASETS])
        table,verdict=assess(pd.concat([self.rows,more],ignore_index=True),self.targets)
        self.assertTrue((table.actual_coverage==.8).all())
        self.assertTrue(verdict['overall_win'] is False) # bad full-coverage score

    def test_contamination_refused(self):
        self.rows.loc[0,'dataset']='kangCrossCell'
        with self.assertRaises(ValueError):assess(self.rows,self.targets)

    def test_nonfinite_refused(self):
        self.rows.loc[0,'certificate']=np.nan
        with self.assertRaises(ValueError):assess(self.rows,self.targets)

if __name__=='__main__':unittest.main()
