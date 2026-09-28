import tempfile
from pathlib import Path
import unittest
import anndata as ad
import numpy as np
from scipy import sparse
from scripts.build_dev_pseudobulk import build


class DevPseudobulkTest(unittest.TestCase):
    def test_sparse_stream_matches_naive(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'nadig25hepg2_processed_complete.h5ad'
            matrix=np.arange(30,dtype=np.float32).reshape(6,5)
            a=ad.AnnData(X=sparse.csr_matrix(matrix))
            a.obs['perturbation']=['control','A','A','B','control','B']
            a.write_h5ad(path)
            result=Path(folder)/'means.npz'
            build(path,result,2)
            with np.load(result) as z:
                for label in ['A','B','control']:
                    where=z['labels'].tolist().index(label)
                    np.testing.assert_array_equal(z['mean_expression'][where],
                                                  matrix[np.array(a.obs.perturbation)==label].mean(axis=0))
            with self.assertRaises(ValueError):
                build(Path(folder)/'nadig25jurkat_processed_complete.h5ad',result)

if __name__=='__main__': unittest.main()
