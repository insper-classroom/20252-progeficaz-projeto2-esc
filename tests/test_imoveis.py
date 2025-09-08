import pytest

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_imoveis(client):
    response = client.get("/imoveis")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
    
