from pathlib import Path
import yaml

from models import Registry, ProjectBinding
from exceptions import RegistryNotFound, InvalidRegistry

ROOT = Path(__file__).resolve().parent
REGISTRY_FOLDER = ROOT / "registry" / "gcp"

class RegistryReader:

    def __init__(self):
        self.registry_folder = REGISTRY_FOLDER

    def find_by_project(self, project_id: str) -> Registry:

        for file in self.registry_folder.glob("*.yaml"):

            with open(file, "r") as f:
                data = yaml.safe_load(f)

            bindings = data.get("bindings", {}).get("gcp", [])

            for binding in bindings:

                if binding["projectId"] == project_id:

                    return Registry(
                        application=data["application"],
                        team=data["team"],
                        owner=data["owner"],
                        budget_owner=data["budgetOwner"],
                        organisation=data["organization"],
                        department=data["department"],
                        cost_center=data["costCenter"],
                        bindings=[
                            ProjectBinding(
                                project_id=b["projectId"],
                                environment=b["environment"],
                                region=b["region"],
                            )
                            for b in bindings
                        ],
                    )

        raise RegistryNotFound(project_id)