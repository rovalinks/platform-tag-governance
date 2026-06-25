#!/usr/bin/env python3

"""
Enterprise GCP Application Registry Validator

This script validates all registry files under:

registry/gcp/

Validation Rules
----------------
1. YAML syntax
2. Mandatory fields
3. Mandatory GCP binding fields
4. Empty values
5. Filename == product
6. Allowed environment
7. Allowed businessCriticality
8. Allowed region
9. Duplicate products
10. Duplicate project IDs
"""

import sys
from pathlib import Path

import yaml


# ==========================================================
# Configuration
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

REGISTRY_PATH = ROOT / "registry" / "gcp"

ALLOWED_VALUES = ROOT / "validation" / "allowed-values.yaml"


# ==========================================================
# Load Allowed Values
# ==========================================================

def load_allowed_values():

    with open(ALLOWED_VALUES, "r") as f:
        return yaml.safe_load(f)


# ==========================================================
# Required Fields
# ==========================================================

REQUIRED_FIELDS = [

    "product",
    "team",
    "owner",
    "budgetOwner",
    "organization",
    "department",
    "costCenter",
    "bindings"

]

REQUIRED_BINDING_FIELDS = [

    "projectId",
    "projectNumber",
    "environment",
    "region",
    "businessCriticality"

]


# ==========================================================
# Validation Helpers
# ==========================================================

def error(message):
    print(f"ERROR : {message}")


def success(message):
    print(f"PASS  : {message}")


# ==========================================================
# Validate One File
# ==========================================================

def validate_file(file_path, allowed_values,
                  products, projects):

    try:

        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

    except Exception as e:
        error(f"{file_path.name} : Invalid YAML ({e})")
        return False

    valid = True

    # ------------------------------------------------------
    # Mandatory Fields
    # ------------------------------------------------------

    for field in REQUIRED_FIELDS:

        if field not in data:

            error(f"{file_path.name} : Missing '{field}'")
            valid = False

    if not valid:
        return False

    # ------------------------------------------------------
    # Empty Values
    # ------------------------------------------------------

    for field in REQUIRED_FIELDS:

        if data.get(field) in [None, ""]:

            error(f"{file_path.name} : Empty '{field}'")
            valid = False

    # ------------------------------------------------------
    # Filename Validation
    # ------------------------------------------------------

    filename = file_path.stem

    if filename != data["product"]:

        error(
            f"{file_path.name} : Filename must match product"
        )

        valid = False

    # ------------------------------------------------------
    # Duplicate Product
    # ------------------------------------------------------

    if data["product"] in products:

        error(
            f"{file_path.name} : Duplicate product '{data['product']}'"
        )

        valid = False

    else:

        products.add(data["product"])

    # ------------------------------------------------------
    # GCP Bindings
    # ------------------------------------------------------

    bindings = data["bindings"].get("gcp", [])

    if not bindings:

        error(f"{file_path.name} : No GCP bindings found")
        return False

    for binding in bindings:

        for field in REQUIRED_BINDING_FIELDS:

            if field not in binding:

                error(
                    f"{file_path.name} : Missing binding field '{field}'"
                )

                valid = False

            elif binding[field] in [None, ""]:

                error(
                    f"{file_path.name} : Empty '{field}'"
                )

                valid = False

        # --------------------------------------------------
        # Duplicate Project
        # --------------------------------------------------

        project = binding["projectId"]

        if project in projects:

            error(
                f"{file_path.name} : Duplicate project '{project}'"
            )

            valid = False

        else:

            projects.add(project)

        # --------------------------------------------------
        # Environment
        # --------------------------------------------------

        if binding["environment"] not in allowed_values["environments"]:

            error(
                f"{file_path.name} : Invalid environment '{binding['environment']}'"
            )

            valid = False

        # --------------------------------------------------
        # Region
        # --------------------------------------------------

        if binding["region"] not in allowed_values["regions"]:

            error(
                f"{file_path.name} : Invalid region '{binding['region']}'"
            )

            valid = False

        # --------------------------------------------------
        # Business Criticality
        # --------------------------------------------------

        if binding["businessCriticality"] not in allowed_values["businessCriticality"]:

            error(
                f"{file_path.name} : Invalid businessCriticality '{binding['businessCriticality']}'"
            )

            valid = False

    if valid:

        success(file_path.name)

    return valid


# ==========================================================
# Main
# ==========================================================

def main():

    allowed_values = load_allowed_values()

    registry_files = sorted(REGISTRY_PATH.glob("*.yaml"))

    if not registry_files:

        error("No registry files found.")

        sys.exit(1)

    print()

    print("=" * 65)
    print(" Enterprise GCP Registry Validation")
    print("=" * 65)
    print()

    products = set()

    projects = set()

    overall = True

    for registry in registry_files:

        if not validate_file(
            registry,
            allowed_values,
            products,
            projects,
        ):

            overall = False

    print()

    print("=" * 65)

    if overall:

        success("All registry files passed validation.")

        print("=" * 65)

        sys.exit(0)

    else:

        error("Validation failed.")

        print("=" * 65)

        sys.exit(1)


if __name__ == "__main__":
    main()