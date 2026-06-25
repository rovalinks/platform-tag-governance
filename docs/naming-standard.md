# Enterprise GCP Registry Naming Standards

## Purpose

This document defines naming conventions for registry files and metadata.

Consistent naming improves automation, readability, and governance.

---

# Registry File Names

Each registry file represents one application.

Format

```
<product>.yaml
```

Examples

```
payments.yaml
sap.yaml
customer-api.yaml
finance-api.yaml
```

Invalid

```
Payments.yaml
SAP.yaml
Finance API.yaml
My Project.yaml
```

---

# Product

Rules

- Lowercase only
- Hyphen (-) allowed
- No spaces
- Must be unique

Examples

```
payments
sap
customer-api
finance-platform
```

---

# Team

Use the owning engineering team.

Examples

```
cloud-platform-engineering
payments-platform
finance-platform
```

---

# Project IDs

Project IDs must match the existing GCP project.

Examples

```
payments-dev
payments-test
payments-prod
```

---

# Environment

Allowed values

```
sandbox
dev
test
uat
prod
```

---

# Region

Use official GCP region names.

Examples

```
europe-west2
europe-west1
us-central1
us-east1
```

---

# Business Criticality

Allowed values

```
low
medium
high
critical
```

---

# Cost Centre

Use the enterprise cost centre.

Examples

```
CC1001
CC2005
FIN001
```

---

# Naming Best Practices

✔ One application per file

✔ Lowercase only

✔ Hyphen-separated names

✔ No spaces

✔ Keep names short and meaningful

✔ Product name must match the filename