"""Frozen v1.0 selective cross-context transfer rules; no held-out data access.

Array axes: rows = training contexts, columns = aligned genes. A perturbation's
training delta is treated pseudobulk minus matched control pseudobulk. All model
fits use only those rows; the target context supplies controls, never outcomes.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class TransferResult:
    predicted_delta: np.ndarray
    certificate: float
    contexts_used: int
    minimum_perturbed_cells: int


def transfer_certificate(deltas: np.ndarray, counts: np.ndarray) -> float:
    """Mean pairwise Pearson across training deltas, shrunk by min(n,2000)/(min(n,2000)+5)."""
    d = np.asarray(deltas, dtype=np.float64)
    n = np.asarray(counts, dtype=np.int64)
    if d.ndim != 2 or n.shape != (d.shape[0],) or d.shape[0] < 2:
        raise ValueError('Need >=2 context deltas and one positive cell count per context')
    if not np.isfinite(d).all() or (n <= 0).any():
        raise ValueError('Nonfinite deltas or nonpositive counts')
    centered = d - d.mean(axis=1, keepdims=True)
    norm = np.linalg.norm(centered, axis=1)
    # Undefined Pearson is not evidence of transfer: lowest possible score.
    similarities = []
    for i in range(len(d)):
        for j in range(i+1, len(d)):
            similarities.append(float(centered[i] @ centered[j] / norm[i] / norm[j])
                                if norm[i] > 0 and norm[j] > 0 else -1.0)
    q = min(int(n.min()), 2000)
    return float(np.mean(similarities) * q/(q+5))


def ridge_corrected_transfer(deltas: np.ndarray, controls: np.ndarray,
                             target_control: np.ndarray, counts: np.ndarray) -> TransferResult:
    """Equal-context mean + per-gene ridge(lambda=1) fitted on train-context LOCO residuals.

    For each training context i, residual_i = actual_delta_i - mean(delta_{j!=i}).
    Regress these residuals per gene on context-control offset from mean control.
    This uses only training contexts, fixed lambda and seed-independent algebra.
    """
    d = np.asarray(deltas, dtype=np.float64)
    c = np.asarray(controls, dtype=np.float64)
    t = np.asarray(target_control, dtype=np.float64)
    n = np.asarray(counts, dtype=np.int64)
    if d.ndim != 2 or c.shape != d.shape or t.shape != (d.shape[1],):
        raise ValueError('Expected context-by-gene arrays and target-control vector')
    if d.shape[0] < 3:
        raise ValueError('At least three training contexts required for LOCO ridge')
    if not (np.isfinite(d).all() and np.isfinite(c).all() and np.isfinite(t).all()):
        raise ValueError('Nonfinite expression')
    center = c.mean(axis=0)
    x = c - center
    residual = d - (d.sum(axis=0, keepdims=True)-d)/(len(d)-1)
    # Independent one-dimensional Ridge per gene with intercept; fixed lambda=1.
    xc = x - x.mean(axis=0)
    yc = residual - residual.mean(axis=0)
    slope = (xc*yc).sum(axis=0)/((xc*xc).sum(axis=0)+1.0)
    correction = residual.mean(axis=0) + (t-center)*slope
    predicted = d.mean(axis=0) + correction
    return TransferResult(predicted, transfer_certificate(d,n), len(d), int(n.min()))


def retain_at_80_percent(scores: np.ndarray, keys: list[str]) -> np.ndarray:
    """Stable rank gate: abstain floor(0.2*n) lowest scores; key tie break."""
    s = np.asarray(scores, dtype=np.float64)
    if s.ndim != 1 or len(s) != len(keys) or len(set(keys)) != len(keys):
        raise ValueError('Scores and unique keys required')
    if not np.isfinite(s).all():
        raise ValueError('Scores must be finite')
    abstain = set(sorted(range(len(s)), key=lambda i:(s[i],keys[i]))[:len(s)//5])
    return np.array([i not in abstain for i in range(len(s))], dtype=bool)
