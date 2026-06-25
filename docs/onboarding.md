# Enterprise GCP Application Onboarding Guide

## Overview

This guide explains how application teams register a new application in the Enterprise GCP Application Registry.

---

# Step 1

Clone the repository.

```
git clone <repository-url>
```

---

# Step 2

Create a new branch.

Example

```
feature/register-payments
```

---

# Step 3

Copy the application template.

```
templates/application-template.yaml
```

Rename the file.

Example

```
payments.yaml
```

Move the file into

```
registry/gcp/
```

---

# Step 4

Populate all mandatory metadata.

Example

```yaml
product: payments

team: payments-platform

owner: payments@company.com

budgetOwner: finance@company.com

organization: rba

department: finance

costCenter: CC1001

bindings:

  gcp:

    - projectId: payments-prod
      environment: prod
      region: europe-west2
      businessCriticality: critical
```

---

# Step 5

Commit the changes.

Example

```
git add .

git commit -m "Register Payments application"
```

---

# Step 6

Push the branch.

```
git push
```

---

# Step 7

Create a Pull Request.

The automated validation pipeline will verify:

- YAML syntax
- Required fields
- Duplicate products
- Duplicate project IDs
- Naming standards

---

# Step 8

Platform Engineering reviews the Pull Request.

If approved, the Pull Request is merged.

---

# Step 9

The application is now registered.

Future platform services will use the registry for:

- Project onboarding
- Governance
- Compliance
- Terraform automation
- Reporting
- Label management

---

# Support

For assistance, contact the Cloud Platform Engineering team.