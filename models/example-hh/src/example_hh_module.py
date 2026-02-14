"""Example model entrypoint for models monorepo validation."""


def create_model(**kwargs):
    """Return a lightweight object for static entrypoint checks."""
    return {"name": "example-hh", "kwargs": kwargs}
