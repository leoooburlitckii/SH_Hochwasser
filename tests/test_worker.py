from unittest.mock import Mock, patch

import requests

import worker

class FakeStation:
    def __init__(self, uuid: str, name: str):
        self.uuid = uuid
        self.name = name

STATION_A = FakeStation(uuid="uuid-a", name="Station A")
STATION_B = FakeStation(uuid="uuid-b", name="Station B")


def make_response(data):
    response = Mock()
    response.json.return_value = data
    return response


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_valid_measurements_are_saved(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response(
        [{"value": 120, "timestamp": "2026-01-01T10:00:00+01:00"}]
    )

    worker.fetch_and_store()

    uuid, measurements = save_mock.call_args.args
    assert uuid == "uuid-a"
    assert measurements[0]["value"] == 120
    assert measurements[0]["timestamp"].year == 2026


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_measurement_without_value_is_skipped(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([
        {"timestamp": "2026-01-01T10:00:00+01:00"},  # kein "value"
        {"value": 130, "timestamp": "2026-01-01T11:00:00+01:00"},
    ])

    worker.fetch_and_store()

    measurements = save_mock.call_args.args[1]
    assert len(measurements) == 1
    assert measurements[0]["value"] == 130


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_measurement_without_timestamp_is_skipped(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([
        {"value": 100},  # kein "timestamp"
        {"value": 130, "timestamp": "2026-01-01T11:00:00+01:00"},
    ])

    worker.fetch_and_store()

    measurements = save_mock.call_args.args[1]
    assert len(measurements) == 1
    assert measurements[0]["value"] == 130


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_measurement_with_wrong_timestamp_is_skipped(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([
        {"value": 100, "timestamp": "not-a-date"},  # kein gültiges Datum
        {"value": 130, "timestamp": "2026-01-01T11:00:00+01:00"},
    ])

    worker.fetch_and_store()

    measurements = save_mock.call_args.args[1]
    assert len(measurements) == 1
    assert measurements[0]["value"] == 130


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_network_error_does_not_stop_other_stations(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A, STATION_B]
    get_mock.side_effect = [
        requests.ConnectionError("down"),
        make_response([{"value": 90, "timestamp": "2026-01-01T10:00:00+01:00"}]),
    ]

    worker.fetch_and_store()

    save_mock.assert_called_once()
    assert save_mock.call_args.args[0] == "uuid-b"


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_http_error_does_not_stop_other_stations(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A, STATION_B]

    broken_response = make_response([])
    broken_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    get_mock.side_effect = [
        broken_response,
        make_response([{"value": 90, "timestamp": "2026-01-01T10:00:00+01:00"}]),
    ]

    worker.fetch_and_store()

    save_mock.assert_called_once()
    assert save_mock.call_args.args[0] == "uuid-b"


@patch("worker.save_measurements_batch")
@patch("worker.requests.get")
@patch("worker.get_all_stations")
def test_database_error_does_not_stop_other_stations(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A, STATION_B]
    get_mock.return_value = make_response(
        [{"value": 90, "timestamp": "2026-01-01T10:00:00+01:00"}]
    )

    # Erster Aufruf (Station A) wirft einen Fehler, zweiter (Station B) liefert 1 (Anzahl der Gespeicherten Stationen)
    save_mock.side_effect = [Exception("db down"), 1]

    worker.fetch_and_store()

    assert save_mock.call_count == 2
    assert save_mock.call_args.args[0] == "uuid-b"
