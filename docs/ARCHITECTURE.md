# Architecture notes

The system is organised around explicit interfaces:

- **CAD parser:** CAD files -> part and feature records.
- **Graph builder:** records -> typed assembly graph.
- **Planner:** graph + goal + scene observations -> ordered assembly steps.
- **Executor:** current observation + current step -> robot action.
- **Simulator:** applies actions and returns observations/state.
- **Verifier:** state + CAD constraints -> success/failure and diagnostics.
- **Learner:** transitions and verifier rewards -> updated policy.

Keep these interfaces independent so that CAD parsing, planning, simulation and learning can be tested separately.
