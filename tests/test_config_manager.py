import json
from unittest.mock import patch

import pytest

import src.config_manager as config_manager


class FakeStation:
    def __init__(self, uuid: str, name: str, row: int, col: int):
        self.uuid = uuid
        self.name = name
        self.row = row
        self.col = col


STATION_KIEL = FakeStation(uuid="u1", name="Kiel", row=5, col=7)
STATION_HUSUM = FakeStation(uuid="u2", name="Husum", row=3, col=2)


@pytest.fixture
def config_file(tmp_path, monkeypatch):
    path = tmp_path / "user_test_config.json"
    monkeypatch.setattr(config_manager, "CONFIG_FILE", str(path))
    return path


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_selected_station_is_saved(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL, STATION_HUSUM]
    input_mock.side_effect = ["1", "K", ""]

    config_manager.configure_stations()

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert saved == [{"symbol": "K", "name": "Kiel", "uuid": "u1", "row": 5, "col": 7}]


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_duplicate_symbol_is_rejected(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL, STATION_HUSUM]
    input_mock.side_effect = ["1", "K", "2", "K", "H", ""]

    config_manager.configure_stations()

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert [s["symbol"] for s in saved] == ["K", "H"]


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_invalid_input_saves_nothing(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL, STATION_HUSUM]
    input_mock.side_effect = ["abc", "99", "0", ""]

    config_manager.configure_stations()

    assert not config_file.exists()


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_same_station_cannot_be_added_twice(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL, STATION_HUSUM]
    
    input_mock.side_effect = ["1", "K", "1", ""]

    config_manager.configure_stations()

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert [s["uuid"] for s in saved] == ["u1"]


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_symbol_with_wrong_length_is_rejected(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL]
    
    input_mock.side_effect = ["1", "KK", "", "K", ""]

    config_manager.configure_stations()

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert [s["symbol"] for s in saved] == ["K"]


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_umlauts_are_saved_unescaped(stations_mock, input_mock, config_file):
    stations_mock.return_value = [FakeStation(uuid="u3", name="Büsum", row=4, col=1)]
    input_mock.side_effect = ["1", "B", ""]

    config_manager.configure_stations()

    # Rohtext prüfen: "ü" muss direkt im File stehen
    assert "Büsum" in config_file.read_text(encoding="utf-8")


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_spaces_around_input_are_ignored(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL]
    input_mock.side_effect = [" 1 ", " K ", ""]

    config_manager.configure_stations()

    saved = json.loads(config_file.read_text(encoding="utf-8"))
    assert saved[0]["symbol"] == "K"
    assert saved[0]["uuid"] == "u1"


@patch("builtins.input")
@patch("src.config_manager.get_all_stations")
def test_existing_config_is_kept_when_nothing_selected(stations_mock, input_mock, config_file):
    stations_mock.return_value = [STATION_KIEL, STATION_HUSUM]
    old_content = '[{"symbol": "H", "name": "Husum", "uuid": "u2", "row": 3, "col": 2}]'
    config_file.write_text(old_content, encoding="utf-8")
    input_mock.side_effect = [""]

    config_manager.configure_stations()

    assert config_file.read_text(encoding="utf-8") == old_content
