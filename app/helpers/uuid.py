import uuid


def generate_uuid():
    """
    Generates a UUID string with hyphens removed.

    Returns:
        str: A unique identifier string.

    This function generates a universally unique identifier (UUID),
    which is then used as a primary key for certain database tables.
    """
    return str(uuid.uuid4()).replace("-", "")
