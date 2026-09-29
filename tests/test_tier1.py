import unittest
import numpy as np
import pandas as pd
from scipy import sparse
from anndata import AnnData
from selective_transfer.tier1 import grouped_means,predict,score_predictions,frozen_keys

class Tier1Test(unittest.TestCase):
    def test_stream_prediction_and_outcome_boundary(self):
        a=AnnData(X=sparse.csr_matrix(np.array([
            [1,2,3],[3,5,5],  # A control, perturb
            [2,3,4],[5,8,7],  # B control, perturb
            [4,5,6],[8,8,13]  # C control, perturb
        ],dtype=np.float32)))
        a.obs['condition1']=['A','A','B','B','C','C']
        a.obs['condition2']=['control','drug']*3
        means,counts=grouped_means(a,2)
        keys=pd.DataFrame([{'outSample':'C','perturb':'drug'}])
        prediction=predict(keys,means,counts)
        self.assertEqual(prediction[0][4],2)
        self.assertIn(('C','drug'),means)
        scored=score_predictions(prediction,means)
        self.assertEqual(len(scored),1)
        self.assertTrue(np.isfinite(scored.iloc[0].mse))
        self.assertTrue(np.isfinite(scored.iloc[0].pcc_delta))

    def test_contaminated_keys_refused(self):
        df=pd.DataFrame([{'DataSet':'kangCrossCell','method':'trainMean',
                          'metric':'pearson_distance','DEG':5000,
                          'outSample':'A','perturb':'drug'}])
        with self.assertRaisesRegex(ValueError,'Contaminated'):
            frozen_keys(df,'kangCrossCell')

    def test_single_context_fallback(self):
        means={('A','control'):np.array([1.,2.,3.]),
               ('A','drug'):np.array([2.,4.,6.]),
               ('B','control'):np.array([3.,4.,5.])}
        counts={k:5 for k in means}
        p=predict(pd.DataFrame([{'outSample':'B','perturb':'drug'}]),means,counts)
        np.testing.assert_array_equal(p[0][2],[1,2,3])
        self.assertEqual(p[0][3],-1.)
        with self.assertRaisesRegex(ValueError,'Missing held-out outcome'):
            score_predictions(p,means)

if __name__=='__main__':unittest.main()
