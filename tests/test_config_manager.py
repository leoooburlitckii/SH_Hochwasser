import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

import config_manager

STATIONS = [
    SimpleNamespace(uuid="u1", name="Kiel", row=5, col=7),
    SimpleNamespace(uuid="u2", name="Husum", row=3, col=2),
]


@pytest.fixture
def config_file(tmp_path, monkeypatch):
    # Test writes into a temp folder, never into the real data/ folder
    path = tmp_path / "user_config.json"
    monkeypatch.setattr(config_manager, "CONFIG_FILE", str(path))
    return path


def run_with_inputs(inputs):
    with patch("config_manager.get_all_stations", return_value=STATIONS), \
         patch("builtins.input", side_effect=inputs):
        config_manager.configure_stations()


def test_selected_station_is_saved(config_file):
    run_with_inputs(["1", "K", ""])

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert saved == [{"symbol": "K", "name": "Kiel", "uuid": "u1", "row": 5, "col": 7}]


def test_duplicate_symbol_is_rejected(config_file):
    # second station first tries "K" again, then gets "H"
    run_with_inputs(["1", "K", "2", "K", "H", ""])

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert [s["symbol"] for s in saved] == ["K", "H"]


def test_invalid_input_saves_nothing(config_file):
    run_with_inputs(["abc", "99", "0", ""])

    assert not config_file.exists()
