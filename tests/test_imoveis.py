import pytest
from unittest.mock import patch, MagicMock
from servidor import connect_db

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_conexao_db_mock():
    fake_conn = MagicMock()
    fake_conn.is_connected.return_value = True
    with patch("servidor.mysql.connector.connect", return_value=fake_conn):
        conn = connect_db()
        assert conn.is_connected()

def test_conexao_db():
    conn = None 
    try:
        conn = connect_db()
        assert conn.is_connected()
    finally:
        if conn:
            conn.close()
        
    


@patch('servidor.connect_db')
def test_get_imoveis(mock_connect_db,client):
    
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Rua A", "Rua", "Bairro A", "Cidade A", "12345-678", "Apartamento", 300000.00, "2023-01-01"),
        (2, "Avenida B", "Avenida", "Bairro B", "Cidade B", "23456-789", "Casa", 500000.00, "2022-06-15")
    ]
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis")
    
    expected_data = [
        {
            "id": 1,
            "logradouro": "Rua A",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro A",
            "cidade": "Cidade A",
            "cep": "12345-678",
            "tipo": "Apartamento",
            "valor": 300000.00,
            "data_aquisicao": "2023-01-01"
        },
        {
            "id": 2,
            "logradouro": "Avenida B",
            "tipo_logradouro": "Avenida",
            "bairro": "Bairro B",
            "cidade": "Cidade B",
            "cep": "23456-789",
            "tipo": "Casa",
            "valor": 500000.00,
            "data_aquisicao": "2022-06-15"
        }
    ]
    assert response.status_code == 200
    assert response.get_json() == expected_data
@patch('servidor.connect_db')
def test_imovel_lista_vazia(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum Imóvel encontrado"}
    
@patch('servidor.connect_db')
def test_imovel_detail(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor 
    
    mock_cursor.fetchone.return_value = [{"id":1, "logradouro":"Rua A","tipo_logradouro": "Rua", "bairro":"Bairro A", "cidade":"Cidade A", "cep":"12345-678", "tipo":"Apartamento", "valor":300000.00, "data_aquisicao":"2023-01-01"}]
    mock_connect_db.return_value = mock_conn
    response = client.get(f"/imoveis/{1}")
    expected_data = [
        {
            "id": 1,
            "logradouro": "Rua A",
            "tipo_logradouro": "Rua",
            "bairro": "Bairro A",
            "cidade": "Cidade A",
            "cep": "12345-678",
            "tipo": "Apartamento",
            "valor": 300000.00,
            "data_aquisicao": "2023-01-01"
        }]
    assert response.status_code == 200
    assert response.get_json() == expected_data
    
    
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
    
    
    
