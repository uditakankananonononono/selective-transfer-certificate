"""Known-outcome development contrasts, not independent confirmation."""
import numpy as np
import pandas as pd
from .core import retain_at_80_percent
from .evaluation import CLEAN_DATASETS


def utility(method,baseline):
    keys=['dataset','context','perturbation']
    for frame in [method,baseline]:
        if frame.duplicated(keys).any():raise ValueError('Duplicate unit')
        if set(frame.dataset)!=CLEAN_DATASETS:raise ValueError('Wrong population')
        if not np.isfinite(frame.pcc_delta).all() or not frame.pcc_delta.between(-1,1).all():
            raise ValueError('Invalid PCC')
    if set(map(tuple,method[keys].to_numpy())) != set(map(tuple,baseline[keys].to_numpy())):
        raise ValueError('Exact key mismatch')
    z=method.merge(baseline[keys+['pcc_delta']],on=keys,validate='one_to_one',suffixes=('','_baseline'))
    tables=[];composition=[];units=[]
    for ds,g in z.groupby('dataset'):
        g=g.copy()
        k=[f'{p}\0{c}' for p,c in zip(g.perturbation,g.context)]
        keep=retain_at_80_percent(g.certificate.to_numpy(),k)
        g['retained']=keep;units.append(g)
        full=float((1-g.pcc_delta).mean());ret=float((1-g.loc[keep,'pcc_delta']).mean())
        baseline_ret=float((1-g.loc[keep,'pcc_delta_baseline']).mean())
        tables.append(dict(dataset=ds,units=len(g),retained=int(keep.sum()),actual_coverage=float(keep.mean()),
                           selector_identifiable=bool((~keep).any()),random_expected_method_risk=full,
                           retained_method_risk=ret,matched_mask_baseline_risk=baseline_ret,
                           selector_risk_improvement=full-ret,matched_predictor_risk_improvement=baseline_ret-ret,
                           selector_descriptive_improvement=bool(ret<full) if (~keep).any() else False,
                           matched_predictor_not_worse=bool(ret<=baseline_ret),
                           full_method_mse=float(g.mse.mean()),retained_method_mse=float(g.loc[keep,'mse'].mean())))
        for context,part in g.groupby('context'):
            composition.append(dict(dataset=ds,context=context,units=len(part),retained=int(part.retained.sum()),
                                    actual_coverage=float(part.retained.mean()),
                                    full_method_pcc=float(part.pcc_delta.mean()),
                                    retained_method_pcc=float(part.loc[part.retained,'pcc_delta'].mean()) if part.retained.any() else None))
    table=pd.DataFrame(tables)
    random=float(table.random_expected_method_risk.mean());retained=float(table.retained_method_risk.mean())
    base=float(table.matched_mask_baseline_risk.mean())
    reduction=(random-retained)/random if random>0 else None
    verdict=dict(design='known-outcome development, finite benchmark panel only',
                 datasets=len(table),units=len(z),selector_identifiable_datasets=int(table.selector_identifiable.sum()),
                 random_expected_macro_method_risk=random,retained_macro_method_risk=retained,
                 matched_mask_macro_baseline_risk=base,relative_selector_risk_reduction=reduction,
                 clause_A_pass=bool(reduction is not None and reduction>=.1),clause_B_pass=bool(retained<=base),
                 descriptive_combined_pass=bool(reduction is not None and reduction>=.1 and retained<=base),
                 independent_invention_win=False)
    return table,pd.DataFrame(composition),pd.concat(units,ignore_index=True),verdict
