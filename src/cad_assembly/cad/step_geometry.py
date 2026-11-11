
import math
import re


def references(entity):
    """Extract referenced STEP entity IDs."""
    refs = []

    for argument in entity["arguments"]:
        refs.extend(
            int(value)
            for value in re.findall(r"#(\d+)", argument)
        )

    return refs


def parse_vector(entity):
    """Extract three numeric coordinates from a STEP point or direction."""
    if not entity or len(entity["arguments"]) < 2:
        raise ValueError("Invalid point or direction entity")

    values = re.findall(
        r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[Ee][-+]?\d+)?",
        entity["arguments"][1]
    )

    if len(values) != 3:
        raise ValueError(f"Expected 3 coordinates, got {values}")

    return [float(value) for value in values]


def normalize(vector):
    magnitude = math.sqrt(sum(value * value for value in vector))

    if magnitude < 1e-12:
        raise ValueError("Cannot normalize a zero-length vector")

    return [value / magnitude for value in vector]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def extract_coordinate_frame(frame_id, entities):
    """Reconstruct an orthonormal frame from AXIS2_PLACEMENT_3D."""

    frame = entities.get(frame_id)

    if not frame or frame["type"] != "AXIS2_PLACEMENT_3D":
        raise ValueError(
            f"Entity #{frame_id} is not AXIS2_PLACEMENT_3D"
        )

    refs = references(frame)

    if len(refs) < 3:
        raise ValueError(f"Incomplete coordinate frame #{frame_id}")

    origin = parse_vector(entities[refs[0]])
    z_axis = normalize(parse_vector(entities[refs[1]]))
    x_reference = normalize(parse_vector(entities[refs[2]]))

    # Orthogonalise X against Z.
    projection = dot(x_reference, z_axis)

    x_axis = normalize([
        x_reference[i] - projection * z_axis[i]
        for i in range(3)
    ])

    y_axis = normalize(cross(z_axis, x_axis))

    return {
        "frame_id": frame_id,
        "origin_mm": origin,
        "x_axis": x_axis,
        "y_axis": y_axis,
        "z_axis": z_axis,
    }
    