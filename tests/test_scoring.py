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

class FullGeneScoreTest(unittest.TestCase):
    def test_fullcell_pcc_mse_and_rounding(self):
        from selective_transfer.scoring import score_verified_payload
        from scipy.stats import pearsonr
        class Data:
            n_vars=5000
            var_names=[str(i) for i in range(5000)]
            obs=pd.DataFrame({'condition1':['A']*4,'condition2':['control','control','drug','drug']})
            X=np.array([np.zeros(5000),np.ones(5000),np.arange(5000)*.01,np.arange(5000)*.02])
        pred=np.arange(5000)*.014 + np.sin(np.arange(5000))*.1
        payload={'dataset':'Afriat','genes':Data.var_names,'rows':[
            {'context':'A','perturbation':'drug','delta':pred.tolist(),
             'certificate':-1.,'training_contexts':1}]}
        actual=np.arange(5000)*.015-.5
        out=score_verified_payload(Data(),payload).iloc[0]
        self.assertEqual(out.pcc_delta,round(float(pearsonr(pred,actual).statistic),4))
        self.assertEqual(out.mse,round(float(np.square(pred-actual).mean()),4))
    def test_undefined_metric_not_dropped(self):
        from selective_transfer.scoring import score_verified_payload
        class Data:
            n_vars=5000
            var_names=[str(i) for i in range(5000)]
            obs=pd.DataFrame({'condition1':['A','A'],'condition2':['control','drug']})
            X=np.zeros((2,5000))
        payload={'dataset':'Afriat','genes':Data.var_names,'rows':[
            {'context':'A','perturbation':'drug','delta':[0.]*5000,
             'certificate':-1.,'training_contexts':1}]}
        with self.assertRaisesRegex(ValueError,'Undefined metric'):
            score_verified_payload(Data(),payload)
