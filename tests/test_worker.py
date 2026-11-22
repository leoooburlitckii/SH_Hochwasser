from unittest.mock import Mock, patch

import requests

import src.worker as worker

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


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
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


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
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


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
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


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
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


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_measurement_with_null_timestamp_is_skipped(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([
        {"value": 100, "timestamp": None},  
        {"value": 130, "timestamp": "2026-01-01T11:00:00+01:00"},
    ])

    worker.fetch_and_store()

    save_mock.assert_called_once()
    measurements = save_mock.call_args.args[1]
    assert len(measurements) == 1
    assert measurements[0]["value"] == 130


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_network_error_does_not_stop_other_stations(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A, STATION_B]
    get_mock.side_effect = [
        requests.ConnectionError("down"),
        make_response([{"value": 90, "timestamp": "2026-01-01T10:00:00+01:00"}]),
    ]

    worker.fetch_and_store()

    save_mock.assert_called_once()
    assert save_mock.call_args.args[0] == "uuid-b"


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
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
    assert get_mock.call_count == 2


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_database_error_does_not_stop_other_stations(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A, STATION_B]
    get_mock.return_value = make_response(
        [{"value": 90, "timestamp": "2026-01-01T10:00:00+01:00"}]
    )

    # Erster Aufruf (Station A) wirft einen Fehler, zweiter (Station B) liefert 1 (Anzahl der Gespeicherten Messungen)
    save_mock.side_effect = [Exception("db down"), 1]

    worker.fetch_and_store()

    assert save_mock.call_count == 2
    assert save_mock.call_args.args[0] == "uuid-b"


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_empty_api_response_saves_nothing(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([])  # API liefert eine leere Liste

    worker.fetch_and_store()

    save_mock.assert_not_called()


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_request_uses_correct_url_and_timeout(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([])

    worker.fetch_and_store()

    expected_url = (
        "https://pegelonline.wsv.de/webservices/rest-api/v2/"
        "stations/uuid-a/W/measurements.json?start=P31D"
    )
    get_mock.assert_called_once_with(expected_url, timeout=10)


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_no_stations_makes_no_requests(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [] 

    worker.fetch_and_store()

    get_mock.assert_not_called()
    save_mock.assert_not_called()


@patch("src.worker.save_measurements_batch")
@patch("src.worker.requests.get")
@patch("src.worker.get_all_stations")
def test_measurement_with_null_value_is_skipped(stations_mock, get_mock, save_mock):
    stations_mock.return_value = [STATION_A]
    get_mock.return_value = make_response([
        {"value": None, "timestamp": "2026-01-01T10:00:00+01:00"},  # value ist null
        {"value": 130, "timestamp": "2026-01-01T11:00:00+01:00"},
    ])

    worker.fetch_and_store()

    save_mock.assert_called_once()
    measurements = save_mock.call_args.args[1]
    assert len(measurements) == 1
    assert measurements[0]["value"] == 130
