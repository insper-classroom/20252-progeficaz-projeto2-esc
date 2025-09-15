import pytest
from unittest.mock import patch, MagicMock



@patch("servidor.connect_db")
def test_listar_todos_os_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchall.return_value = [
        {
            "id": 1, "logradouro": "Rua A", "tipo_logradouro": "Rua",
            "bairro": "Bairro A", "cidade": "Cidade A",
            "cep": "12345-678", "tipo": "Apartamento",
            "valor": 300000.00, "data_aquisicao": "2023-01-01"
        }
    ]

    resp = client.get("/imoveis")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert data[0]["id"] == 1
    assert data[0]["tipo"] == "Apartamento"
    assert "_links" in data[0]


@patch("servidor.connect_db")
def test_listar_todos_os_imoveis_erro_conexao(mock_connect_db, client):
    mock_connect_db.return_value = None
    resp = client.get("/imoveis")
    assert resp.status_code == 500
    assert resp.get_json() == {"erro": "Erro ao conectar ao banco de dados"}


@patch("servidor.connect_db")
def test_obter_imovel_por_id_encontrado(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchone.return_value = {
        "id": 10, "logradouro": "Rua X", "tipo_logradouro": "Rua",
        "bairro": "Centro", "cidade": "São Paulo",
        "cep": "01000-000", "tipo": "Apartamento",
        "valor": 999999.99, "data_aquisicao": "2024-05-10"
    }

    resp = client.get("/imoveis/10")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 10
    assert data["tipo"] == "Apartamento"
    assert "_links" in data


@patch("servidor.connect_db")
def test_obter_imovel_por_id_nao_encontrado(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.fetchone.return_value = None

    resp = client.get("/imoveis/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Imóvel não encontrado"}


@patch("servidor.connect_db")
def test_buscar_imovel_por_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchall.return_value = [
        {
            "id": 1, "logradouro": "Rua A", "tipo_logradouro": "Rua",
            "bairro": "Bairro A", "cidade": "Cidade A",
            "cep": "12345-678", "tipo": "Apartamento",
            "valor": 300000.00, "data_aquisicao": "2023-01-01"
        }
    ]

    resp = client.get("/imoveis/tipo/Apartamento")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert data[0]["tipo"] == "Apartamento"
    assert "_links" in data[0]


@patch("servidor.connect_db")
def test_buscar_imovel_por_tipo_nao_encontrado(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.fetchall.return_value = []

    resp = client.get("/imoveis/tipo/Chacara")
    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Nenhum Imóvel encontrado"}


@patch("servidor.connect_db")
def test_buscar_imovel_por_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchall.return_value = [
        {
            "id": 1, "logradouro": "Rua A", "tipo_logradouro": "Rua",
            "bairro": "Bairro A", "cidade": "São Paulo",
            "cep": "12345-678", "tipo": "Apartamento",
            "valor": 300000.00, "data_aquisicao": "2023-01-01"
        }
    ]

    resp = client.get("/imoveis/cidade/São Paulo")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert data[0]["cidade"] == "São Paulo"
    assert "_links" in data[0]


@patch("servidor.connect_db")
def test_buscar_imovel_por_cidade_sem_resultados(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.fetchall.return_value = []

    resp = client.get("/imoveis/cidade/NaoExiste")
    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Nenhum Imóvel encontrado"}


@patch("servidor.connect_db")
def test_buscar_imovel_por_cidade_erro_conexao(mock_connect_db, client):
    mock_connect_db.return_value = None
    resp = client.get("/imoveis/cidade/São Paulo")
    assert resp.status_code == 500
    assert resp.get_json() == {"erro": "Erro ao conectar ao banco de dados"}


# -----------------------------
# Rotas de ESCRITA (patch função)
# -----------------------------

@patch("servidor.novo_imovel")
def test_criar_imovel_sucesso(mock_novo_imovel, client):
    payload = {
        "logradouro": "Rua Nova", "tipo_logradouro": "Rua", "bairro": "Centro",
        "cidade": "São Paulo", "cep": "01010-010", "tipo": "Apartamento",
        "valor": 450000.00, "data_aquisicao": "2024-01-20"
    }
    retornado = {**payload, "id": 123, "_links": {"self": "/imoveis/123"}}
    mock_novo_imovel.return_value = (retornado, 201)

    resp = client.post("/imoveis", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["id"] == 123
    assert "_links" in data


@patch("servidor.novo_imovel")
def test_criar_imovel_invalido(mock_novo_imovel, client):
    mock_novo_imovel.return_value = ({"erro": "Dados inválidos ou incompletos"}, 400)
    resp = client.post("/imoveis", json={"logradouro": "faltando campos"})
    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "Dados inválidos ou incompletos"}


@patch("servidor.editar_imovel")
def test_atualizar_imovel_sucesso(mock_editar_imovel, client):
    imovel_id = 10
    payload = {
        "logradouro": "Rua X", "tipo_logradouro": "Rua", "bairro": "Centro",
        "cidade": "São Paulo", "cep": "01000-000", "tipo": "Apartamento",
        "valor": 480000.00, "data_aquisicao": "2024-05-10"
    }
    atualizado = {**payload, "id": imovel_id, "_links": {"self": f"/imoveis/{imovel_id}"}}
    mock_editar_imovel.return_value = (atualizado, 200)

    resp = client.put(f"/imoveis/{imovel_id}", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == imovel_id
    assert data["valor"] == 480000.00
    assert "_links" in data


@patch("servidor.editar_imovel")
def test_atualizar_imovel_nao_encontrado(mock_editar_imovel, client):
    mock_editar_imovel.return_value = ({"erro": "Imóvel não encontrado"}, 404)
    resp = client.put("/imoveis/9999", json={"valor": 1})
    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Imóvel não encontrado"}


@patch("servidor.delete_imovel")
def test_remover_imovel_sucesso(mock_delete_imovel, client):
    mock_delete_imovel.return_value = ({"mensagem": "Imóvel deletado com sucesso", "id": 10}, 200)
    resp = client.delete("/imoveis/10")
    assert resp.status_code == 200
    assert resp.get_json() == {"mensagem": "Imóvel deletado com sucesso", "id": 10}


@patch("servidor.delete_imovel")
def test_remover_imovel_nao_encontrado(mock_delete_imovel, client):
    mock_delete_imovel.return_value = ({"erro": "Imóvel não encontrado"}, 404)
    resp = client.delete("/imoveis/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Imóvel não encontrado"}
