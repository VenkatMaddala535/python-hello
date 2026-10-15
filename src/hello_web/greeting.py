"""A small function with observable behavior to test in Jenkins."""


def greeting(name: str = "") -> str:
    """To greet person."""
    cleaned = name.strip()
    if len(cleaned) > 80:
        raise ValueError("Please use a name with 80 characters or fewer.")
    return f"Hello, {cleaned or 'World'}!"
