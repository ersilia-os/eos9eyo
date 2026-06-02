\
"""Quality-weighted consensus across LazyQSAR sub-models.

Mirrors chembl-antimicrobial-models/scripts/14_consensus_scoring.py:
- W1..W7 are per-sub-model quality weights from reports.csv.
- W8 is a per-compound weight that ramps 0->1 above each sub-model's
  decision_cutoff_rank.
- All 8 weights are uniformly averaged into an effective per-compound,
  per-sub-model weight; the consensus is the weighted mean of prob_ranks;
  a tanh transform then restores the IQR that averaging compresses
  toward 0.5.

NaN policy: if any sub-model returns NaN for a given compound, that
compound's consensus_score is NaN (no weighting, no averaging). The
per-sub-model columns keep the real prob_ranks where prediction succeeded
and NaN where it did not.
"""

import os
import numpy as np
import pandas as pd

_W_COLS = ["w1", "w2", "w3", "w4", "w5", "w6", "w7"]
_TANH_A, _TANH_TAU = 1.2421278739876145, 10.621775439578736


def compute_consensus(R, cols_ordered, model_names, checkpoints_dir):
    """Build the model's output matrix.

    Args:
        R:               (n, K) prob_rank matrix returned by lqsar_predict.
        cols_ordered:    list of K column names matching R's columns (also from lqsar_predict).
        model_names:     canonical sub-model order for this pathogen (length M, M <= K).
        checkpoints_dir: path to model/checkpoints/ (must contain reports.csv).

    Returns:
        results: (n, 1+M) float array, rounded to 4 decimals.
                 results[:, 0] is the tanh-transformed consensus score.
                 results[:, 1:] is the per-sub-model prob_rank reordered to match model_names.
        header:  ["consensus_score", *model_names].
    """
    name_to_idx = {c: i for i, c in enumerate(cols_ordered)}
    prob_ranks = R[:, [name_to_idx[m] for m in model_names]].astype(float)

    # Single sub-model: the consensus would just be a tanh-rescaled copy of
    # the sole prob_rank. Skip it and emit only the sub-model column.
    if len(model_names) == 1:
        return np.round(prob_ranks, 4), list(model_names)

    reports = pd.read_csv(os.path.join(checkpoints_dir, "reports.csv")).set_index("model_name")
    w_quality = np.array([reports.loc[m, _W_COLS].values for m in model_names], dtype=float)
    cutoffs   = np.array([reports.loc[m, "decision_cutoff_rank"] for m in model_names], dtype=float)

    # Compounds with any NaN prob_rank get consensus = NaN; the rest go
    # through the full weighting+tanh pipeline. Splitting like this keeps
    # the NaN policy explicit and avoids invalid-value runtime warnings.
    n, M = prob_ranks.shape
    nan_rows  = np.isnan(prob_ranks).any(axis=1)
    consensus = np.full(n, np.nan)

    if (~nan_rows).any():
        pr = prob_ranks[~nan_rows]
        c  = np.clip(cutoffs[np.newaxis, :], 0.0, 1.0 - 1e-9)
        w8 = np.where(pr <= c, 0.0, (pr - c) / (1.0 - c))

        n_good = pr.shape[0]
        n_w    = len(_W_COLS) + 1
        w_all = np.empty((n_good, M, n_w))
        w_all[:, :, :len(_W_COLS)] = w_quality
        w_all[:, :,  len(_W_COLS)] = w8
        w_eff = np.average(w_all, axis=-1, weights=np.ones(n_w))

        raw = (pr * w_eff).sum(axis=1) / w_eff.sum(axis=1)
        k   = 2.0 * (1.0 + _TANH_A * (1.0 - np.exp(-M / _TANH_TAU)))
        consensus[~nan_rows] = 0.5 + 0.5 * np.tanh(k * (raw - 0.5)) / np.tanh(k / 2)

    results = np.round(np.column_stack([consensus, prob_ranks]), 4)
    header  = ["consensus_score", *model_names]
    return results, header
