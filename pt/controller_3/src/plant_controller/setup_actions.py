from typing import Any

class HasSetupFunctionsMixin:
    """
    Mixin for classes that have setup functions.
    """
    def setup_functions(self) -> dict[str, dict[str, Any]]:
        return {}