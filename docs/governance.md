# Enterprise GCP Application Registry Governance

## Purpose

The Enterprise GCP Application Registry is the single source of truth for application metadata used across Google Cloud Platform (GCP).

The registry standardises application ownership, project metadata, cost allocation, governance, and future automation.

---

# Objectives

- Standardise application metadata across GCP.
- Enable consistent project onboarding.
- Improve governance and compliance.
- Support future automation (Terraform, Project Factory, Labeling).
- Reduce manual effort and configuration drift.

---

# Registry Principles

## One Application = One Registry File

Each application must have its own YAML file.

Example

```
payments.yaml
customer-api.yaml
sap.yaml
```

Do not store multiple applications in the same file.

---

## File Location

```
registry/gcp/
```

---

## Source of Truth

The registry is the authoritative source for:

- Product
- Team
- Owner
- Budget Owner
- Department
- Cost Centre
- Project Mapping
- Environment
- Business Criticality

---

## Mandatory Fields

The following fields are mandatory.

| Field | Required |
|---------|----------|
| product | Yes |
| team | Yes |
| owner | Yes |
| budgetOwner | Yes |
| organization | Yes |
| department | Yes |
| costCenter | Yes |
| bindings.gcp.projectId | Yes |
| bindings.gcp.environment | Yes |
| bindings.gcp.region | Yes |
| bindings.gcp.businessCriticality | Yes |

---

## Pull Request Process

Every registry change must be submitted using a Pull Request.

All Pull Requests must:

- Pass automated validation.
- Be reviewed by the Platform Engineering team.
- Be approved before merging.

---

## Validation Rules

Registry validation will verify:

- YAML syntax
- Mandatory fields
- Duplicate products
- Duplicate Project IDs
- Allowed values
- Naming conventions

---

## Future Enhancements

Future phases may include:

- Project Factory integration
- Terraform automation
- Automatic project labels
- Cloud Asset Inventory integration
- Compliance dashboards
- Automated remediation