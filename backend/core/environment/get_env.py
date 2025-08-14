from __future__ import annotations

import os
from builtins import str as str_type
from typing import TYPE_CHECKING, NoReturn, TypeVar, cast

from exceptions import MissingEnvironmentVariableError

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")


class GetEnv:
    """
    Helper class for retrieving and validating environment variables.

    Supports generic type casting with type safety using modern Python
    type hints.
    """

    @staticmethod
    def raise_error(key: str) -> NoReturn:
        """Always raise a MissingEnvironmentVariableError for a given key."""
        msg = f"{key} is required but not set."
        raise MissingEnvironmentVariableError(msg)

    @staticmethod
    def get(
        key: str,
        cast_to: Callable[[str], T],
        default: T | None = None,
        separator: str | None = None,
    ) -> T:
        """
        Retrieve and cast an environment variable to the desired type.

        Args:
            key: Environment variable name.
            cast_to: Function that casts the string to the target type.
            default: Value to return if the environment variable is missing.
            separator: If provided, splits the string before casting (for lists).

        Returns:
            The casted value of the environment variable.

        Raises:
            MissingEnvironmentVariableError: If missing and no default is given.
            ValueError: If casting fails.

        """
        raw_value = os.getenv(key)

        if raw_value is None or raw_value.strip() == "":
            if default is None:
                GetEnv.raise_error(key)
            return default

        if separator:
            # Example: cast_to = str, separator = "," → list[str]
            parts = [p.strip() for p in raw_value.split(separator) if p.strip()]
            return cast("T", [cast_to(p) for p in parts])  # type: ignore  # noqa: PGH003

        return cast_to(raw_value)

    # Convenience wrappers
    @staticmethod
    def str(key: str, default: str | None = None) -> str:
        return GetEnv.get(key, str, default)

    @staticmethod
    def int(key: str_type, default: int | None = None) -> int:
        return GetEnv.get(key, int, default)

    @staticmethod
    def float(key: str_type, default: float | None = None) -> float:
        return GetEnv.get(key, float, default)

    @staticmethod
    def bool(key: str_type, default: bool | None = None) -> bool:
        def to_bool(v: str) -> bool:
            return v.strip().lower() in {"1", "true", "yes", "on"}

        return GetEnv.get(key, to_bool, default)

    @staticmethod
    def list(
        key: str_type,
        cast_to: Callable[[str_type], T] | type[str_type] = str_type,
        default: list[T] | None = None,
        separator: str_type = ",",
    ) -> list[T]:
        return GetEnv.get(key, cast_to, default, separator)  # type: ignore  # noqa: PGH003
