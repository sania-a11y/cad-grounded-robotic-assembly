# CAD-Grounded Robotic Assembly

**Ontology-Guided Knowledge Graphs for VLM-Based Assembly Planning and Simulated Robotic Execution**

This research project explores how structured knowledge extracted from 3D CAD assemblies can improve vision-language-based robotic assembly planning and execution.

The proposed framework combines STEP-based CAD parsing, ontology engineering, Knowledge Graph construction, Vision-Language Models (VLMs), and simulator-in-the-loop verification to support reliable robotic sub-assembly.

## Research Motivation

Robotic assembly requires more than visual recognition. A robot must identify components, understand their structural relationships, interpret spatial configurations, generate valid assembly plans, and verify whether the intended operations have been completed successfully.

CAD files contain valuable engineering information, including component definitions, assembly hierarchy, occurrences, and geometric placements. However, this information is not always directly accessible to vision-language models in a structured and semantically meaningful form.

This project investigates whether representing CAD-derived information through an ontology-guided Knowledge Graph can improve assembly planning reliability and simulated robotic execution.

## Research Question

**Does grounding VLM-based assembly planning in an ontology-guided Knowledge Graph derived from CAD data improve planning reliability and simulated robotic assembly performance compared with using equivalent structured CAD information without an explicit graph?**

## Proposed Architecture

The proposed workflow consists of the following stages:

1. **CAD / STEP Parsing**
   - Extract product and component definitions.
   - Identify assembly occurrences and hierarchy.
   - Extract placement and transformation relationships.
   - Reconstruct component coordinate frames.

2. **Ontology Engineering**
   - Develop a domain-specific CAD assembly ontology.
   - Represent assemblies, components, occurrences, placements, and coordinate frames.
   - Define semantic constraints using SHACL.

3. **Knowledge Graph Construction**
   - Generate RDF representations using RDFLib.
   - Validate graph structure and semantic constraints.
   - Store and query assembly knowledge using Neo4j.

4. **Knowledge-Grounded VLM Planning**
   - Combine visual observations and natural-language instructions.
   - Retrieve relevant assembly knowledge from the Knowledge Graph.
   - Generate structured assembly plans.
   - Investigate parameter-efficient VLM fine-tuning where appropriate.

5. **Robotic Execution and Verification**
   - Integrate a compatible pretrained Vision-Language-Action (VLA) policy.
   - Execute assembly plans in a simulation environment.
   - Verify component placement, alignment, collisions, and task completion.
   - Explore policy adaptation and reinforcement learning where feasible.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| CAD processing | STEP / ISO 10303 |
| Knowledge representation | RDF, RDFLib, Turtle |
| Ontology validation | SHACL, pySHACL |
| Graph database | Neo4j |
| Machine learning | PyTorch, Transformers |
| Vision-language models | Pretrained VLMs |
| Robotic learning | VLA policies, Behaviour Cloning, optional RL |
| Simulation | To be selected based on robot and policy compatibility |
| Development | VS Code, Git, GitHub |

## Repository Structure

```text
cad-grounded-robotic-assembly/
│
├── configs/
│   └── example_assembly.json
│
├── data/
│   ├── raw/
│   │   └── cad/
│   └── processed/
│
├── ontology/
│   └── cad_assembly_ontology.ttl
│
├── src/
│   └── cad_assembly/
│       └── cad/
│           ├── step_inventory.py
│           └── step_geometry.py
│
├── scripts/
│   └── validate_graph.py
│
├── tests/
│
├── README.md
└── .gitignore
```

*The structure will evolve as ontology construction, graph generation, VLM planning, and simulation modules are implemented.*

## Current Progress

### Implemented

- [x] Python project environment and dependencies.
- [x] STEP entity inventory extraction.
- [x] Product and component definition identification.
- [x] Assembly occurrence and hierarchy extraction.
- [x] Mapping of 59 assembly occurrences to transformation relationships.
- [x] Initial coordinate-frame reconstruction.
- [x] Example assembly JSON validation.
- [x] Initial parser tests.

### In Progress / Planned

- [ ] CAD assembly ontology development.
- [ ] RDF Knowledge Graph generation.
- [ ] SHACL-based semantic validation.
- [ ] Neo4j integration and graph queries.
- [ ] CAD-grounded VLM planning.
- [ ] Structured assembly-plan generation.
- [ ] VLA integration and simulated robotic execution.
- [ ] Simulator-based verification and evaluation.
- [ ] Fine-tuning and policy adaptation experiments.

## Experimental Design

The proposed evaluation will compare different levels of CAD grounding:

- **Baseline 1:** Vision-only pretrained VLM.
- **Baseline 2:** VLM with structured CAD information in JSON format.
- **Proposed approach:** VLM grounded through an ontology-guided Knowledge Graph.

Evaluation will investigate:

- Component identification accuracy.
- Assembly relationship prediction.
- Valid assembly plan generation.
- Constraint violations.
- Component placement and orientation errors.
- Collision frequency.
- Simulated task success rate.
- Execution time and robustness.

Controlled experiments and ablation studies will help determine whether explicit Knowledge Graph grounding provides measurable benefits over alternative representations.

## Research Scope

The initial implementation focuses on extracting and representing reliable information from STEP-based CAD assemblies. Subsequent stages will investigate how this information can support knowledge-grounded assembly planning and robotic execution.

Mechanical mating relationships, assembly sequences, and physical constraints will only be represented when supported by appropriate geometric or engineering evidence.

## Project Status

**Research prototype — active development.**

This repository documents the implementation and experimental development of the proposed CAD-grounded robotic assembly framework.

## Author

**Sania Verma**

MSc Artificial Intelligence  
City St George's, University of London

- Github : [@sania-a11y](https://github.com/sania-a11y)
- Portfolio: [sania8.github.io/website](https://sania8.github.io/website)

---

*This project is being developed as part of an ongoing research investigation into Knowledge Graph-grounded multimodal AI and robotic assembly.*