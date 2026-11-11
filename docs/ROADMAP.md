# Roadmap

## Phase 0 — setup
- [ ] Create GitHub repository
- [ ] Create Python environment and install package
- [ ] Confirm CAD data permissions and obtain STEP exports
- [ ] Select the first 3–5 parts and document the assembly goal

## Phase 1 — E1: CAD to knowledge graph
- [ ] Define part/feature/fastener schema
- [ ] Import STEP geometry and extract available metadata
- [ ] Create graph relations: `requires`, `precedes`, `fits`, `fastened_by`
- [ ] Add rule-based consistency checks
- [ ] Create manual ground-truth labels
- [ ] Evaluate feature and relation precision/recall/F1

## Phase 2 — E2: assembly planning
- [ ] Implement a rule-based baseline
- [ ] Add a prompted VLM planner using graph + scene context
- [ ] Validate plan ordering and fit constraints
- [ ] Compare graph-grounded and graph-free planning

## Phase 3 — E3: synthetic perception
- [ ] Render labelled synthetic images
- [ ] Randomise lighting, camera pose and background
- [ ] Train/evaluate a part detector on held-out renders
- [ ] Test on real photos only if permitted and available

## Phase 4 — E4: simulation and imitation
- [ ] Choose one simulator and pin its version
- [ ] Build a minimal scene and robot reachability test
- [ ] Generate scripted demonstrations
- [ ] Establish an imitation-learning baseline

## Phase 5 — E5: simulator-reward RL
- [ ] Implement binary verified-success reward
- [ ] Add shaped reward only as a documented ablation
- [ ] Compare RL policy against the E4 supervised baseline
- [ ] Track success versus rollout/sample count

## Phase 6 — E6: generalisation
- [ ] Hold out part geometry, pose, lighting and clearance conditions
- [ ] Evaluate generalisation gap
- [ ] Consider real-robot validation only if hardware and permissions exist
