import unittest
import numpy as np
from selective_transfer.core import ridge_corrected_transfer, transfer_certificate, retain_at_80_percent


class CoreTest(unittest.TestCase):
    def test_concordance(self):
        same = np.array([[2.,3.,4.],[4.,5.,6.]])
        opposite = np.array([[2.,3.,4.],[4.,3.,2.]])
        self.assertAlmostEqual(transfer_certificate(same,np.array([5,9])),.5)
        self.assertAlmostEqual(transfer_certificate(opposite,np.array([5,9])),-.5)

    def test_zero_vector_is_lowest_not_nan(self):
        d=np.array([[0.,0.,0.],[1.,2.,3.]])
        self.assertAlmostEqual(transfer_certificate(d,np.array([5,5])),-.5)

    def test_training_only_and_per_gene_ridge(self):
        d=np.array([[1.,2.,3.],[2.,4.,6.],[3.,6.,9.]])
        c=np.array([[1.,1.,1.],[2.,2.,2.],[3.,3.,3.]])
        r=ridge_corrected_transfer(d,c,np.array([4.,4.,4.]),np.array([12,16,20]))
        self.assertEqual(r.contexts_used,3)
        self.assertEqual(r.minimum_perturbed_cells,12)
        self.assertEqual(r.predicted_delta.shape,(3,))
        self.assertTrue(np.isfinite(r.predicted_delta).all())
        self.assertTrue(np.isfinite(r.certificate))
        with self.assertRaises(ValueError):
            ridge_corrected_transfer(d[:2],c[:2],np.array([4.,4.,4.]),np.array([12,16]))

    def test_abstention_exact_when_divisible_by_five(self):
        s=np.array([.2,.1,.4,.7,.8,.9,.5,.6,.3,.0])
        retain=retain_at_80_percent(s,[str(i) for i in range(10)])
        self.assertEqual(retain.sum(),8)
        self.assertFalse(retain[9]);self.assertFalse(retain[1])

    def test_ties_independent_of_input_order(self):
        first=retain_at_80_percent(np.ones(5),['z','a','b','c','d'])
        self.assertEqual(first.tolist(),[True,False,True,True,True])

if __name__=='__main__': unittest.main()
