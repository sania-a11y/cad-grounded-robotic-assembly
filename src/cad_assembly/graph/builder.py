import networkx as nx

from cad_assembly.graph.schema import AssemblySpec


def build_graph(spec: AssemblySpec) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph(assembly_id=spec.assembly_id, goal=spec.goal)
    for part in spec.parts:
        graph.add_node(part.id, **part.model_dump())
    for relation in spec.relations:
        graph.add_edge(
            relation.source,
            relation.target,
            relation=relation.type,
        )
    return graph
