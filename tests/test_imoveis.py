import pytest

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_imoveis(client):
    response = client.get("/imoveis")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
    
def test_imovel_detail(client):
    response = client.get("/imoveis/1")
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert "logradouro" in response.json
    assert "tipo_logradouro" in response.json
    assert "bairro" in response.json
    assert "cidade" in response.json
    assert "cep" in response.json
    assert "tipo" in response.json
    assert "valor" in response.json
    assert "data_aquisicao" in response.json
    
    
def test_criar_imoveis(client):
    payload = {
        "logradouro": "Rua Teste",
        "tipo_logradouro": "Rua",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "Apartamento",
        "valor": 250000.00,
        "data_aquisicao": "2023-01-01"
    }
    response = client.post("/imoveis", json=payload)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["logradouro"] == payload["logradouro"]
    assert response.json["tipo_logradouro"] == payload["tipo_logradouro"]
    assert response.json["bairro"] == payload["bairro"]
    assert response.json["cidade"] == payload["cidade"]
    assert response.json["cep"] == payload["cep"]
    assert response.json["tipo"] == payload["tipo"]
    assert response.json["valor"] == payload["valor"]
    assert response.json["data_aquisicao"] == payload["data_aquisicao"]
    res2 = client.get("/imoveis")
    data2 = res2.get_json()
    assert data2["count"] == 1
    assert data2["items"][0]["cep"] == "12345-678"
    
    
    
