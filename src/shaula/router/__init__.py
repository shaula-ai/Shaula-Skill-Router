"""
shaula-skill-router — Production-grade tool routing for AI agents.

Quick usage::

    # Route an intent to a CLI
    from shaula import router
    result = router.route("查上週銷售總額")

    # Validate a manifest you wrote
    from shaula.router import validator
    r = validator.validate_file("my-tool.json")
    if not r.ok:
        for e in r.errors: print("ERROR:", e)

The package makes no external API calls. Path B of the router returns
empty params; the caller decides how to fill them.
"""

from shaula.router.router import CLIbrary
from shaula.router import validator

__version__ = "0.2.1"


class _DefaultRouter:
    """Lazy-initialized default router. Forwards every attribute to a real
    ``CLIbrary`` instance built on first access."""

    __slots__ = ("_impl",)

    def __init__(self) -> None:
        self._impl = None

    def _get(self) -> CLIbrary:
        if self._impl is None:
            self._impl = CLIbrary()
        return self._impl

    def __getattr__(self, name):
        return getattr(self._get(), name)

    def __repr__(self) -> str:
        state = "loaded" if self._impl is not None else "not loaded yet"
        return f"<shaula.router.router default CLIbrary ({state})>"


_default_router = _DefaultRouter()


def route(query: str):
    """Route an intent using the lazily initialized default router."""
    return _default_router.route(query)

__all__ = ["CLIbrary", "route", "validator"]
