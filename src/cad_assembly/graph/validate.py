from cad_assembly.graph.schema import AssemblySpec

ALLOWED_RELATIONS = {"requires", "precedes", "fits", "fastened_by"}


def validate_assembly(spec: AssemblySpec) -> list[str]:
    errors: list[str] = []
    part_ids = {part.id for part in spec.parts}

    if len(part_ids) != len(spec.parts):
        errors.append("Duplicate part IDs found.")

    for relation in spec.relations:
        if relation.type not in ALLOWED_RELATIONS:
            errors.append(f"Unsupported relation type: {relation.type}")
        if relation.source not in part_ids:
            errors.append(f"Unknown relation source: {relation.source}")
        if relation.target not in part_ids:
            errors.append(f"Unknown relation target: {relation.target}")

    return errors
