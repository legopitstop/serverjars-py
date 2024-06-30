__all__ = ["InvalidRequest", "JarNotFoundError"]


class InvalidRequest(Exception):
    pass


class JarNotFoundError(Exception):
    pass
