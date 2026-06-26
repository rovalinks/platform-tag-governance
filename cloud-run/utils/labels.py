def build_labels(registry):

    return {
        "product": registry.product.lower(),
        "team": registry.team.lower(),
        "department": registry.department.lower(),
        "owner": (
            registry.owner.lower()
            .replace("@", "-")
            .replace(".", "-")
        ),
        "costcentre": registry.cost_center.lower(),
    }