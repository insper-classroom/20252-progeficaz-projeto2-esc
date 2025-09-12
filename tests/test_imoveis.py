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
def test_get_imovel_nao_encontrado(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor 
    
    mock_cursor.fetchone.return_value = None
    mock_connect_db.return_value = mock_conn
    response = client.get(f"/imoveis/{100000}")
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imóvel não encontrado"}

    
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
    
@patch('servidor.connect_db')
def test_criar_imoveis(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    response = client.post("/imoveis", json={
        "logradouro": "Rua Teste",
        "tipo_logradouro": "Rua",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "Apartamento",
        "valor": 400000.00,
        "data_aquisicao": "2023-10-01"
    })
    assert response.status_code == 201
    assert response.get_json() == {"mensagem": "Imóvel criado com sucesso"}
    
@pytest.mark.parametrize("resposta, erro, esperado", [
    # faltando logradouro
    (
        {
            "tipo_logradouro": "Rua",
            "bairro": "Bairro Teste",
            "cidade": "Cidade Teste",
            "cep": "12345-678",
            "tipo": "Apartamento",
            "valor": 400000.00,
            "data_aquisicao": "2023-10-01"
        },
        400,
        {"erro": "Dados inválidos ou incompletos"}
    ),
    # valor negativo
    (
        {
            "logradouro": "Rua Teste",
            "bairro": "Bairro Teste",
            "cidade": "Cidade Teste",
            "cep": "12345-678",
            "tipo": "Apartamento",
            "valor": -100.00,
            "data_aquisicao": "2023-10-01"
        },
        400,
        {"erro": "Dados inválidos ou incompletos"}
    ),
    # data em formato errado
    (
        {
            "logradouro": "Rua Teste",
            "bairro": "Bairro Teste",
            "cidade": "Cidade Teste",
            "cep": "12345-678",
            "tipo": "Apartamento",
            "valor": 400000.00,
            "data_aquisicao": "01-10-2023"
        },
        400,
        {"erro": "Dados inválidos ou incompletos"}
    ),
])
@patch('servidor.connect_db')
def test_erro_na_criacao_de_imoveis(mock_connect_db, client, resposta, erro, esperado):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    response = client.post("/imoveis", json=resposta)

    assert response.status_code == erro
    assert response.get_json() == esperado
    
    
    
