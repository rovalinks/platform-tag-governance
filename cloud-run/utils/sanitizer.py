def sanitize_owner(owner):

    return (
        owner.lower()
        .replace("@", "-")
        .replace(".", "-")
    )