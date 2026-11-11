# Experiment plan

| ID | Research question | Baseline | Main metric |
|---|---|---|---|
| E1 | Can CAD be parsed into a correct graph? | Manual graph labels | Feature/relation precision, recall, F1 |
| E2 | Does graph grounding improve VLM plans? | Rule-based oracle; graph-free VLM | Plan validity rate |
| E3 | Can CAD renders train a useful detector? | Real-photo-only detector, if data exists | mAP |
| E4 | How far does imitation learning go? | Scripted controller | Execution success rate |
| E5 | Does simulator-reward RL beat imitation? | E4 supervised policy | Verified insertion success, sample efficiency |
| E6 | Does the system generalise? | Training-distribution performance | Held-out success and generalisation gap |

Use at least five random seeds per condition where compute permits. Keep a fixed evaluation set and report means with 95% bootstrap confidence intervals. Define tolerances per part pair from CAD clearances; do not choose them after observing test results.
