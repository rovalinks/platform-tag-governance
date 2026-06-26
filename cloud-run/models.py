from dataclasses import dataclass


@dataclass
class ProjectBinding:
    project_id: str
    environment: str
    region: str


@dataclass
class Registry:
    product: str
    team: str
    owner: str
    budget_owner: str
    organisation: str
    department: str
    cost_center: str
    bindings: list[ProjectBinding]