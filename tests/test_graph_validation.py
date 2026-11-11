from cad_assembly.graph.schema import AssemblySpec
from cad_assembly.graph.validate import validate_assembly
from cad_assembly.graph.builder import build_graph


def sample_spec():
    return AssemblySpec.model_validate({
        "assembly_id": "test",
        "goal": "Join two parts",
        "parts": [{"id": "plate", "kind": "part"}, {"id": "hub", "kind": "part"}],
        "relations": [{"source": "plate", "type": "fits", "target": "hub"}],
    })


def test_valid_spec_has_no_errors():
    assert validate_assembly(sample_spec()) == []


def test_unknown_part_is_reported():
    spec = sample_spec()
    spec.relations[0].target = "missing"
    assert any("Unknown relation target" in e for e in validate_assembly(spec))


def test_graph_contains_parts_and_relation():
    graph = build_graph(sample_spec())
    assert set(graph.nodes) == {"plate", "hub"}
    assert graph.has_edge("plate", "hub")
