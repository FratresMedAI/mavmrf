# Seeded benchmark

Reproducible simulation-only gate. Regenerate with:

```bash
cd marmf
python scripts/benchmark.py --seed 42 --duration 5 --num-objects 6
```

## Conditions

| Parameter | Value |
|-----------|-------|
| Seed | `42` |
| Duration (sec) | 5 |
| Simulated objects | 6 |
| Filter sensitivity | `medium` |
| Detection source | `simulation` |
| Generated (UTC) | 2026-07-19T17:40:55.885046+00:00 |

## Results

| Metric | Value |
|--------|-------|
| Frames processed | 25 |
| Elapsed (sec) | 0.89 |
| Throughput (frames/sec) | 28.08 |
| Unique track IDs | 6 |
| Total fused observations | 150 |
| Mean fused objects / frame | 6.0 |
| Notifications (total) | 6 |

### Contact types (observation counts)

| Contact type | Count |
|--------------|-------|
| `unknown` | 150 |

Machine-readable copy: [`seeded_run.json`](seeded_run.json).

These numbers are **simulation gates**, not field performance claims.
