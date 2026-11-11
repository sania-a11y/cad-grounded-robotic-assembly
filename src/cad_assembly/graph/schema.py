from pydantic import BaseModel, Field


class Part(BaseModel):
    id: str
    kind: str
    description: str | None = None


class Relation(BaseModel):
    source: str
    type: str
    target: str


class AssemblySpec(BaseModel):
    assembly_id: str
    goal: str
    parts: list[Part] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
