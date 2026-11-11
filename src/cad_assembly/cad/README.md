# CAD ingestion

The first implementation should target STEP (`.step` / `.stp`) exports. Keep the CAD adapter isolated from the graph schema. Before selecting a parser, verify the source CAD format, assembly structure, and required geometric features. Do not assume every STEP file preserves semantic feature-tree information such as tapped-hole labels.
