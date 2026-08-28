import pytest

from gamesaver.utils import COLORS, colored, colored_multi


def test_colored_uses_known_color():
    result = colored("green", "ok")
    assert COLORS["GREEN"] in result
    assert "ok" in result


def test_colored_defaults_to_white_for_unknown_color():
    result = colored("unknown", "text")
    assert COLORS["WHITE"] in result
    assert "text" in result


def test_colored_multi_joins_segments():
    result = colored_multi(["red", "green"], ["a", "b"])
    assert "a" in result
    assert "b" in result


def test_colored_multi_raises_on_mismatched_lengths():
    with pytest.raises(ValueError, match="same size"):
        colored_multi(["red"], ["a", "b"])
