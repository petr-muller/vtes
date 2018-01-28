from unittest.mock import Mock
import pytest
from vtes.run import ParsePlayerAction

def test_parse_players():
    action = ParsePlayerAction(dest="players", option_strings=("players", ))
    namespace = Mock()
    for valid_length in (3, 4, 5, 6):
        action(Mock(), namespace, ["x"] * valid_length)
        assert len(namespace.players) == valid_length

    for invalid_length in (0, 1, 2, 7, 8):
        with pytest.raises(ValueError):
            action(Mock(), namespace, ["x"] * invalid_length)
