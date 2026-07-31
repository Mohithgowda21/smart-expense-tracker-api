
from fastapi.testclient import TestClient
from src.main import app,save

client=TestClient(app)

def setup_function():
    save([])

def test_flow():
    r=client.post("/expenses",json={"title":"Coffee","amount":100,"category":"Food","date":"2026-07-31"})
    assert r.status_code==201
    assert client.get("/expenses").json()[0]["title"]=="Coffee"
    assert client.get("/expenses/total").json()["total"]==100
    assert client.get("/expenses?category=Food").status_code==200
    assert client.get("/expenses/total/Food").json()["total"]==100
    assert client.delete("/expenses/1").status_code==200
