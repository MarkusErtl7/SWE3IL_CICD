from app.main import add, app


def test_add():
    assert add(2, 3) == 5


def test_index():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_health():
    res = app.test_client().get("/health")
    assert res.status_code == 200


def test_add_route():
    res = app.test_client().get("/add/4/5")
    assert res.get_json()["result"] == 9
