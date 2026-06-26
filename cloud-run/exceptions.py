class RegistryError(Exception):
    pass


class RegistryNotFound(RegistryError):
    pass


class InvalidRegistry(RegistryError):
    pass