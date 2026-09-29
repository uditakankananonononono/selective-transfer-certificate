"""Metadata-only plan from frozen public result CSV, no expression outcomes read."""
import argparse
import pandas as pd


def plan(reference):
    df=pd.read_csv(reference)
    z=df[(df.metric=='pearson_distance') & (df.method=='trainMean') & (df.DEG==5000)]
    forbidden={'kangCrossCell'}
    for dataset, subset in z.groupby('DataSet'):
        if dataset in forbidden:
            continue
        contexts=sorted(subset.outSample.unique().tolist())
        perturbations=sorted(subset.perturb.unique().tolist())
        units=list(zip(subset.outSample.tolist(), subset.perturb.tolist()))
        if len(units)!=len(set(units)):
            raise ValueError(f'duplicate dataset target in {dataset}')
        k=len(units)//5
        print(f'{dataset:20s} contexts={len(contexts):2} perts={len(perturbations):3} '
              f'units={len(units):3} abstain={k:2} actual_coverage={(len(units)-k)/len(units):.3f} '
              f'one_context={len(contexts)==2}')

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--reference',required=True)
    plan(a.parse_args().reference)
