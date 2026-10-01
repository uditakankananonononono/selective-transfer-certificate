# Preregistration clarification v1.2 - FROZEN

Dated and frozen October 1, 2026, Asia/Calcutta, before any clean Tier-1
method outcome comparison. This corrects metric logistics, not the invention,
population, targets, model, certificate, retention rule or win bar. v1.0 and
v1.1 remain verbatim. kangCrossCell remains development-only due to contamination.

The pinned published source governs PCC/MSE evaluation:
- Use all cells for PCC and MSE. The source's 2,000-cell subsample applies only
  to distribution metrics, not these metrics.
- Round each unit's PCC/MSE to four decimals before dataset/macro aggregation.
- DEG-5000 is all 5,000 unique aligned genes on a confirmed 5,000-gene input.
  No held-out DEG ranking is used in prediction. Refuse inputs where this
  full-gene-set equivalence cannot be established.

Source pin: 698f8ff5ed19530bff171e4205be9b42a46a769d.
Source calPerformance.py SHA-256:
979efef1f120c60d653080d99b81ac7f373be26886102cb3dcc36ca3aa0f759d.
https://github.com/bm2-lab/scPerturBench/blob/698f8ff5ed19530bff171e4205be9b42a46a769d/Cellular_context_generalization/o.o.d./calPerformance.py

All 11 clean datasets and their exact published targets remain unchanged.
The full-coverage comparison on each dataset and >=10% macro risk reduction
at actual achieved retained coverage both remain mandatory. No clean outcome
was scored before this clarification. Scores and negatives will be reported
without model tuning or population changes.

Owner evidence inspected: authenticated September 28 messages granting research
discretion (8:57:11 PM, 'Genuinely, do whatever you deem fit') and requiring judge
survival (8:59:35 PM). This clarification repairs the mismatch to the named
published source. Parent confirmed this exact clarification on October 1 before
scoring. The repository's text is a record, not independent permission evidence.
