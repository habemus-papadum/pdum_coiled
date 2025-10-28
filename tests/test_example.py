"""Example tests for coiled."""

from pdum import coiled


def test_version():
    """Test that the package has a version."""
    assert hasattr(coiled, "__version__")
    assert isinstance(coiled.__version__, str)
    assert len(coiled.__version__) > 0


def test_import():
    """Test that the package can be imported."""
    assert coiled is not None



def test_widget_payload():
    """Widget helper produces a JSON-serializable payload."""
    widget = coiled.Widget(title="Hello", body="World")
    payload = widget.to_payload()
    assert payload["title"] == "Hello"
    assert payload["body"] == "World"

