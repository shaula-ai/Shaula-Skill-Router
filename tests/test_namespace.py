"""The public namespace API must coexist with independently installed components."""
import importlib
from unittest.mock import Mock, patch

import shaula
from shaula import router


def test_shared_namespace_has_no_root_initializer():
    assert shaula.__file__ is None
    assert router.__name__ == "shaula.router"


def test_package_route_delegates_to_lazy_default():
    implementation = Mock()
    implementation.route.return_value = {"action": "route", "cli": "example"}
    with patch.object(router, "_default_router", implementation):
        assert router.route("example intent")["cli"] == "example"
    implementation.route.assert_called_once_with("example intent")


def test_router_submodule_is_importable():
    module = importlib.import_module("shaula.router.router")
    assert module.CLIbrary is router.CLIbrary


def test_default_index_location_matches_builder():
    from shaula.router.build_index import DEFAULT_OUTPUT_DIR
    assert router.CLIbrary()._index_dir == DEFAULT_OUTPUT_DIR
