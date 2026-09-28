import anndata as ad, numpy as np, pandas as pd
from scipy.stats import pearsonr
p='/tmp/deep-research/algorithm-invention/perturb-seq-track/tier1-data/kangCrossCell.h5ad'
a=ad.read_h5ad(p,backed='r')
obs=a.obs
X=np.asarray(a.X[:], dtype=np.float32)
cs=obs.condition1.to_numpy(); stim=(obs.condition2.to_numpy()=='stimulated'); ctl=~stim
rows=[]
for context in obs.condition1.unique():
 train_mean=X[(cs!=context)&stim].mean(axis=0,dtype=np.float64)
 treat_mean=X[(cs==context)&stim].mean(axis=0,dtype=np.float64)
 control_mean=X[(cs==context)&ctl].mean(axis=0,dtype=np.float64)
 delta_pred=train_mean-control_mean
 delta_true=treat_mean-control_mean
 corr=float(pearsonr(delta_pred,delta_true).statistic)
 rows.append((context,corr,1-corr, int(((cs==context)&ctl).sum()), int(((cs==context)&stim).sum())))
f='/tmp/deep-research/algorithm-invention/perturb-seq-track/baseline-refs/cellular_ood_distance5000.csv'
d=pd.read_csv(f);z=d[(d.DataSet=='kangCrossCell')&(d.method=='trainMean')&(d.metric=='pearson_distance')].set_index('outSample')
for c,r,dist,nc,nt in rows: print(f'{c:12s} corr={r:.4f} dist={dist:.4f} pinned={z.loc[c,"performance"]:.4f} corr_diff={r-z.loc[c,"performance"]:+.4f} nctl={nc} ntreat={nt}',flush=True)
print('MEAN CORR',np.mean([x[1] for x in rows]),'MEAN DIST',np.mean([x[2] for x in rows]),'PINNED',z.performance.mean(),flush=True)
