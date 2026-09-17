import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app  # noqa: E402

client = TestClient(app.app)


def test_health():
    assert client.get('/health').json() == {'status': 'ok'}


def test_ping_parser(monkeypatch):
    class Result:
        returncode = 0
        stdout = '64 bytes from 1.1.1.1: time=12.5 ms\n64 bytes from 1.1.1.1: time=14 ms\n'

    monkeypatch.setattr(app.subprocess, 'run', lambda *args, **kwargs: Result())
    assert app.ping('1.1.1.1', 2) == [12.5, 14.0]


def test_diagnose_shape(monkeypatch):
    monkeypatch.setattr(app, 'gateway', lambda: None)
    monkeypatch.setattr(app.socket, 'getaddrinfo', lambda *args: [])
    monkeypatch.setattr(app, 'ping', lambda *args, **kwargs: [])
    response = client.post('/api/diagnose')
    assert response.status_code == 200
    assert {'Gateway', 'DNS', 'Internet', 'Latency', 'Stability'} <= response.json()['checks'].keys()
