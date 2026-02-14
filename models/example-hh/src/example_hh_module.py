"""Example model entrypoint for biomodels monorepo validation."""


def create_model(**kwargs):
    """Return a lightweight object for static entrypoint checks."""
    return {"name": "example-hh", "kwargs": kwargs}
