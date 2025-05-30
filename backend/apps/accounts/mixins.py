import random
import re
import string
from datetime import datetime

from django.utils.text import slugify


class UniqueUsernameMixin:
    """Mixin to generate a unique username based on the user's email.
    This mixin can be used in Django views or models to ensure that
    the generated username is unique and does not exceed a specified
    length.
    """

    @staticmethod
    def generate_username(email: str, max_length=150) -> str:
        """
        Generate a unique-looking username from an email, without checking the database.
        - Sanitized and slugified.
        - Appends a short timestamp + random digits.
        - Truncated to max_length (default: 150).
        """

        # Extract username from email and sanitize it
        base = slugify(email.split("@")[0])
        base = re.sub(r"[^a-z0-9_-]", "", base)

        # Add a timestamp suffix + 2 random digits (for uniqueness)
        suffix = str(int(datetime.now().timestamp()))[-6:]
        random_digits = "".join(random.choices(string.digits, k=2))

        # Make uniquene user name
        username = f"{base}-{suffix}{random_digits}"

        # Enforce max length
        return username[:max_length]
