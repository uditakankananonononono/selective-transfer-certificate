import copy
import unittest
import numpy as np
import pandas as pd
from selective_transfer.locking import extract_fold, make_lock, verify_lock
from selective_transfer.tier1 import predict

class GuardedMatrix:
    def __init__(self):
        self.data=np.array([[1.,2.,3.],[2.,4.,6.],[3.,4.,5.],[999.,999.,999.]])
    def __getitem__(self, key):
        rows, cols=key
        if 3 in rows:
            raise AssertionError('Held-out treated row accessed')
        return self.data[rows,cols]
class FakeData:
    n_vars=3
    var_names=['g1','g2','g3']
    obs=pd.DataFrame({'condition1':['A','A','B','B'],
                      'condition2':['control','drug','control','drug']})
    X=GuardedMatrix()
class LockTest(unittest.TestCase):
    def setUp(self):
        self.means,self.counts,self.genes=extract_fold(FakeData(),'B',1)
        self.keys=pd.DataFrame([{'outSample':'B','perturb':'drug'}])
        self.pred=predict(self.keys,self.means,self.counts)
        self.lock=make_lock('Afriat',self.keys,self.pred,self.genes,'a'*64,'b'*64,'c'*64)
    def test_never_reads_target_treated(self):
        self.assertNotIn(('B','drug'),self.means)
        np.testing.assert_array_equal(self.pred[0][2],[1,2,3])
    def test_roundtrip(self):
        verify_lock(self.lock,self.keys,self.genes,'a'*64,'b'*64,'c'*64)
    def test_modified_prediction_refused(self):
        z=copy.deepcopy(self.lock); z['payload']['rows'][0]['delta'][0]+=1
        with self.assertRaisesRegex(ValueError,'modified'):
            verify_lock(z,self.keys,self.genes,'a'*64,'b'*64,'c'*64)
    def test_permuted_genes_refused(self):
        with self.assertRaisesRegex(ValueError,'Gene order'):
            verify_lock(self.lock,self.keys,self.genes[::-1],'a'*64,'b'*64,'c'*64)
    def test_wrong_source_refused(self):
        with self.assertRaisesRegex(ValueError,'Provenance'):
            verify_lock(self.lock,self.keys,self.genes,'a'*64,'b'*64,'d'*64)
    def test_contamination_refused(self):
        with self.assertRaisesRegex(ValueError,'clean dataset'):
            make_lock('kangCrossCell',self.keys,self.pred,self.genes,'a'*64,'b'*64,'c'*64)
if __name__=='__main__':unittest.main()
