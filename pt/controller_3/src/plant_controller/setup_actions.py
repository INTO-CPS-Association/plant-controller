"""Mixin for components that expose interactive setup actions."""

from typing import Any


class HasSetupFunctionsMixin:
    """Mixin for classes that provide setup/calibration functions.

    Classes using this mixin can expose named actions to the interactive
    setup utility. Override ``setup_functions`` to return a dict of
    available actions.
    """

    def setup_functions(self) -> dict[str, dict[str, Any]]:
        """Return available setup actions for this component.

        Returns:
            Dict mapping action names to dicts with keys:
                - 'description' (str): Human-readable description.
                - 'function' (async callable): The setup coroutine to run.
            Returns empty dict if no setup actions are available.
        """
        return {}