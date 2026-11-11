
import re
import json
from pathlib import Path
from collections import Counter
from step_geometry import extract_coordinate_frame
import math

STEP_FILE = Path(
    "data/raw/cad/Hub n Adopter_RoboArm_Prototype2_Industrialgrade.STEP"
)

OUTPUT_FILE = Path("data/processed/step_inventory.json")


def split_arguments(text):
    """Split STEP arguments while respecting nested parentheses and strings."""
    args = []
    current = []
    depth = 0
    in_string = False
    i = 0

    while i < len(text):
        char = text[i]

        if char == "'":
            current.append(char)

            if in_string and i + 1 < len(text) and text[i + 1] == "'":
                current.append("'")
                i += 2
                continue

            in_string = not in_string

        elif not in_string:
            if char == "(":
                depth += 1
                current.append(char)
            elif char == ")":
                depth -= 1
                current.append(char)
            elif char == "," and depth == 0:
                args.append("".join(current).strip())
                current = []
            else:
                current.append(char)
        else:
            current.append(char)

        i += 1

    if current:
        args.append("".join(current).strip())

    return args



def extract_entities(step_text):
    """Extract STEP entities using balanced-parenthesis parsing."""
    entities = {}

    start_pattern = re.compile(
        r"#(\d+)\s*=\s*([A-Z0-9_]+)\s*\("
    )

    for match in start_pattern.finditer(step_text):
        entity_id = int(match.group(1))
        entity_type = match.group(2)

        start = match.end()
        depth = 1
        in_string = False
        i = start

        while i < len(step_text) and depth > 0:
            char = step_text[i]

            if char == "'":
                # STEP escapes apostrophes inside strings as two apostrophes.
                if in_string and i + 1 < len(step_text):
                    if step_text[i + 1] == "'":
                        i += 2
                        continue

                in_string = not in_string

            elif not in_string:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1

            i += 1

        if depth != 0:
            continue

        arguments_text = step_text[start:i - 1].strip()

        # Allow whitespace between the closing parenthesis and semicolon.
        j = i
        while j < len(step_text) and step_text[j].isspace():
            j += 1

        if j < len(step_text) and step_text[j] == ";":
            entities[entity_id] = {
                "type": entity_type,
                "arguments": split_arguments(arguments_text)
            }

    return entities


def extract_complex_relationships(step_text):
    """Extract STEP complex representation relationships."""
    relationships = {}

    pattern = re.compile(
        r"#(\d+)\s*=\s*\(\s*REPRESENTATION_RELATIONSHIP\b",
        re.DOTALL
    )

    for match in pattern.finditer(step_text):
        relationship_id = int(match.group(1))

        end = step_text.find(";", match.end())
        if end == -1:
            continue

        block = step_text[match.start():end]

        relationship_match = re.search(
            r"REPRESENTATION_RELATIONSHIP\s*\((.*?)\)"
            r"\s*REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION"
            r"\s*\(\s*#(\d+)\s*\)",
            block,
            re.DOTALL
        )

        if not relationship_match:
            continue

        representation_ids = [
            int(ref)
            for ref in re.findall(
                r"#(\d+)", relationship_match.group(1)
            )
        ]

        transformation_id = int(relationship_match.group(2))

        relationships[relationship_id] = {
            "representations": representation_ids,
            "transformation_id": transformation_id
        }

    return relationships


def references(entity):
    """Return referenced STEP entity IDs."""
    return [
        int(ref)
        for ref in re.findall(r"#(\d+)", " ".join(entity["arguments"]))
    ]


def quoted_name(value):
    """Remove surrounding STEP quotes."""
    value = value.strip()
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def build_inventory(entities):
    # STEP PRODUCT ID -> component name
    products = {}

    for entity_id, entity in entities.items():
        if entity["type"] == "PRODUCT":
            args = entity["arguments"]
            if args:
                products[entity_id] = quoted_name(args[0])

    # PRODUCT_DEFINITION_FORMATION ID -> PRODUCT ID
    formations = {}

    for entity_id, entity in entities.items():
        if entity["type"].startswith("PRODUCT_DEFINITION_FORMATION"):
            for ref in references(entity):
                if ref in products:
                    formations[entity_id] = ref
                    break

    # PRODUCT_DEFINITION ID -> PRODUCT name
    definitions = {}

    for entity_id, entity in entities.items():
        if entity["type"] == "PRODUCT_DEFINITION":
            for ref in references(entity):
                if ref in formations:
                    product_id = formations[ref]
                    definitions[entity_id] = products[product_id]
                    break

    # Extract parent-child assembly occurrences
    occurrences = []

    for entity_id, entity in entities.items():
        if entity["type"] != "NEXT_ASSEMBLY_USAGE_OCCURRENCE":
            continue

        refs = references(entity)

        if len(refs) < 2:
            continue

        parent_id = refs[-2]
        child_id = refs[-1]

        occurrences.append({
            "occurrence_id": entity_id,
            "parent_definition_id": parent_id,
            "child_definition_id": child_id,
            "parent": definitions.get(parent_id, "UNRESOLVED"),
            "child": definitions.get(child_id, "UNRESOLVED")
        })

    component_counts = Counter(
        item["child"] for item in occurrences
    )

    return {
        "product_count": len(products),
        "product_names": list(products.values()),
        "occurrence_count": len(occurrences),
        "component_counts": dict(component_counts),
        "occurrences": occurrences
    }


def main():
    if not STEP_FILE.exists():
        raise FileNotFoundError(
            f"STEP file not found: {STEP_FILE}"
        )

    print("Reading STEP file...")

    step_text = STEP_FILE.read_text(
        encoding="utf-8",
        errors="replace"
    )

    entities = extract_entities(step_text)
    relationships = extract_complex_relationships(step_text)

    print(
        f"Complex representation relationships: {len(relationships)}"
    )

    print(
        "Relationship #1323:",
        relationships.get(1323)
    )

    # Connect each context-dependent representation to its occurrence
    placement_links = []

    for context_id, context in entities.items():
        if context["type"] != "CONTEXT_DEPENDENT_SHAPE_REPRESENTATION":
            continue

        context_refs = references(context)

        if len(context_refs) < 2:
            continue

        relationship_id = context_refs[0]
        product_shape_id = context_refs[1]

        product_shape = entities.get(product_shape_id)

        if not product_shape:
            continue

        shape_refs = references(product_shape)

        occurrence_id = next(
            (
                ref for ref in shape_refs
                if entities.get(ref, {}).get("type")
                == "NEXT_ASSEMBLY_USAGE_OCCURRENCE"
            ),
            None
        )

        relationship = relationships.get(relationship_id)

        if occurrence_id is None or relationship is None:
            continue

        placement_links.append({
            "context_representation_id": context_id,
            "occurrence_id": occurrence_id,
            "relationship_id": relationship_id,
            "transformation_id": relationship["transformation_id"],
            "representation_ids": relationship["representations"]
        })

    print("\nPLACEMENT MAPPING")
    print("-----------------")
    print(f"Successfully mapped placements: {len(placement_links)}")
    print(f"Unique occurrences: {len(set(x['occurrence_id'] for x in placement_links))}")
    print(f"Unique transformations: {len(set(x['transformation_id'] for x in placement_links))}")

    print("\nFirst three mappings:")
    for link in placement_links[:3]:
        print(link)

    # Reconstruct coordinate frames
    print("\nRECONSTRUCTED COORDINATE FRAMES")
    print("--------------------------------")

    print("\nALL PLACEMENT FRAME VALIDATION")
    print("--------------------------------")

    zero_origin_count = 0
    nonzero_origin_count = 0
    checked_frames = 0

    for link in placement_links:
        transformation = entities[link["transformation_id"]]
        frame_ids = references(transformation)

        for frame_id in frame_ids:
            frame = extract_coordinate_frame(frame_id, entities)
            origin = frame["origin_mm"]

            distance = math.sqrt(sum(value ** 2 for value in origin))

            checked_frames += 1

            if distance < 1e-6:
                zero_origin_count += 1
            else:
                nonzero_origin_count += 1

    print(f"Coordinate frames checked: {checked_frames}")
    print(f"Frames at origin: {zero_origin_count}")
    print(f"Frames away from origin: {nonzero_origin_count}")


    for link in placement_links[:3]:
        transformation = entities[link["transformation_id"]]
        frame_ids = references(transformation)

        print(f"\nOccurrence #{link['occurrence_id']}")

        for frame_id in frame_ids:
            frame = extract_coordinate_frame(frame_id, entities)

            print(f"  Frame #{frame_id}")
            print(f"    Origin (mm): {frame['origin_mm']}")
            print(f"    X axis: {frame['x_axis']}")
            print(f"    Y axis: {frame['y_axis']}")
            print(f"    Z axis: {frame['z_axis']}")

    print("\nCOORDINATE FRAME INSPECTION")
    print("---------------------------")

    for link in placement_links[:3]:
        transformation_id = link["transformation_id"]
        transformation = entities.get(transformation_id)

        print(f"\nOccurrence: #{link['occurrence_id']}")
        print(f"Transformation: #{transformation_id}")

        if not transformation:
            print("Transformation entity not found!")
            continue

        frame_ids = references(transformation)
        print(f"Coordinate frame IDs: {frame_ids}")

        for frame_id in frame_ids:
            frame = entities.get(frame_id)

            if not frame:
                print(f"  Frame #{frame_id}: not found")
                continue

            print(f"  Frame #{frame_id}: {frame['type']}")

            if frame["type"] == "AXIS2_PLACEMENT_3D":
                frame_refs = references(frame)
                print(f"    Point/direction references: {frame_refs}")

                for ref_id in frame_refs:
                    referenced_entity = entities.get(ref_id)

                    if referenced_entity:
                        print(
                            f"    #{ref_id}: "
                            f"{referenced_entity['type']} "
                            f"{referenced_entity['arguments']}"
                        )


    print(f"STEP entities extracted: {len(entities)}")
    from collections import Counter

    entity_counts = Counter(
        entity["type"] for entity in entities.values()
    )

    print("\nSPATIAL ENTITY COUNTS")
    print("---------------------")

    for entity_type in [
        "NEXT_ASSEMBLY_USAGE_OCCURRENCE",
        "CONTEXT_DEPENDENT_SHAPE_REPRESENTATION",
        "ITEM_DEFINED_TRANSFORMATION",
        "REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION",
        "PRODUCT_DEFINITION_SHAPE",
        "AXIS2_PLACEMENT_3D",
        "CARTESIAN_POINT",
        "DIRECTION",
    ]:
        print(f"{entity_type}: {entity_counts.get(entity_type, 0)}")


    inventory = build_inventory(entities)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(inventory, indent=4),
        encoding="utf-8"
    )

    print("\nASSEMBLY INVENTORY")
    print("------------------")
    print("Products:", inventory["product_count"])
    print("Occurrences:", inventory["occurrence_count"])

    print("\nComponent counts:")

    for name, count in inventory["component_counts"].items():
        print(f"  {name}: {count}")

    print("\nSaved inventory to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
