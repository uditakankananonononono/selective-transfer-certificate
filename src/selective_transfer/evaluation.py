"""Frozen v1.1 arithmetic: read scored rows ONLY after model predictions are locked.

This module contains pure table calculations, no data downloads and no model
training. It refuses contamination and missing/extra evaluation datasets.
"""
import numpy as np
import pandas as pd
from .core import retain_at_80_percent

CLEAN_DATASETS=frozenset({'Afriat','Haber','KaggleCrossCell','KaggleCrossPatient',
                          'McFarland','Parekh','TCDD','crossPatient','crossSpecies',
                          'kangCrossPatient','sciplex3'})


def assess(scored: pd.DataFrame, frozen_targets: pd.DataFrame) -> tuple[pd.DataFrame,dict]:
    """Rows: dataset, context, perturbation, pcc_delta, mse; targets: dataset,pcc_delta.

    Returns every dataset's full/retained score and honest outcome against the
    frozen trainMean benchmark. PCC is higher-better; risk=1-PCC.
    """
    required={'dataset','context','perturbation','pcc_delta','mse'}
    if not required <= set(scored):
        raise ValueError(f'Missing scored fields {required-set(scored)}')
    if not {'dataset','pcc_delta'} <= set(frozen_targets):
        raise ValueError('Missing frozen target fields')
    if set(scored.dataset) != CLEAN_DATASETS or set(frozen_targets.dataset) != CLEAN_DATASETS:
        raise ValueError('Expected exactly 11 clean evaluation datasets, no contaminated kangCrossCell')
    if scored.duplicated(['dataset','context','perturbation']).any():
        raise ValueError('Duplicate evaluation unit')
    if frozen_targets.dataset.duplicated().any():
        raise ValueError('Duplicate target')
    if not np.isfinite(scored[['pcc_delta','mse']].to_numpy(dtype=float)).all():
        raise ValueError('Nonfinite metric')
    if not np.isfinite(frozen_targets.pcc_delta.to_numpy(dtype=float)).all():
        raise ValueError('Nonfinite target')
    if not scored.pcc_delta.between(-1,1).all():
        raise ValueError('PCC outside [-1,1]')
    if (scored.mse < 0).any():
        raise ValueError('Negative MSE')
    # Evaluator must receive frozen scores, not recalculate from observed outcomes.
    if 'certificate' not in scored or not np.isfinite(scored.certificate.to_numpy(dtype=float)).all():
        raise ValueError('Missing/nonfinite prescored certificate')
    targets=frozen_targets.set_index('dataset').pcc_delta
    rows=[]
    for ds,group in scored.groupby('dataset'):
        keys=[f'{p}\0{c}' for p,c in zip(group.perturbation,group.context)]
        keep=retain_at_80_percent(group.certificate.to_numpy(),keys)
        full=float(group.pcc_delta.mean())
        retained=float(group.loc[keep,'pcc_delta'].mean())
        mse_full=float(group.mse.mean())
        rows.append({'dataset':ds,'units':len(group),'retained':int(keep.sum()),
                     'actual_coverage':float(keep.mean()),'full_pcc_delta':full,
                     'retained_pcc_delta':retained,'full_mse':mse_full,
                     'baseline_pcc_delta':float(targets[ds]),
                     'full_pass':bool(full>=targets[ds])})
    table=pd.DataFrame(rows).sort_values('dataset').reset_index(drop=True)
    base_risk=float((1-table.baseline_pcc_delta).mean())
    method_risk=float((1-table.retained_pcc_delta).mean())
    relative_reduction=(base_risk-method_risk)/base_risk if base_risk>0 else float('nan')
    verdict={'all_full_pass':bool(table.full_pass.all()),
             'baseline_macro_risk':base_risk,'method_macro_risk':method_risk,
             'relative_risk_reduction':relative_reduction,
             'risk_pass':bool(relative_reduction>=0.10),
             'overall_win':bool(table.full_pass.all() and relative_reduction>=0.10)}
    return table,verdict
