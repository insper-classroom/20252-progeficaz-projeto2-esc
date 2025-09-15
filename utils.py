from datetime import datetime
from urllib.parse import quote

def format_imovel(imovel):
    tipo_encoded = quote(str(imovel["tipo"]))
    cidade_encoded = quote(str(imovel["cidade"]))
    return {
        "id": imovel["id"],
        "logradouro": imovel["logradouro"],
        "tipo_logradouro": imovel["tipo_logradouro"],
        "bairro": imovel["bairro"],
        "cidade": imovel["cidade"],
        "cep": imovel["cep"],
        "tipo": imovel["tipo"],
        "valor": float(imovel["valor"]),
        "data_aquisicao": str(imovel["data_aquisicao"]),
        "_links": {
            "self": f"/imoveis/{imovel['id']}",
            "update": f"/imoveis/{imovel['id']}",
            "delete": f"/imoveis/{imovel['id']}",
            "by_tipo": f"/imoveis/tipo/{tipo_encoded}",
            "by_cidade": f"/imoveis/cidade/{cidade_encoded}"
        }
    }


def novo_imovel(data):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    required_fields = ("logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao")
    if not data or not isinstance(data, dict) or not all(field in data for field in required_fields):
        return {"erro": "Dados inválidos ou incompletos"}, 400

    if not isinstance(data["valor"], (int, float)) or data["valor"] <= 0:
        return {"erro": "Dados inválidos ou incompletos"}, 400

    try:
        datetime.strptime(data["data_aquisicao"], "%Y-%m-%d")
    except Exception:
        return {"erro": "Dados inválidos ou incompletos"}, 400

    cursor = conn.cursor()
    try:
        sql = """INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            data["logradouro"], data["tipo_logradouro"], data["bairro"], data["cidade"],
            data["cep"], data["tipo"], data["valor"],
            datetime.strptime(data["data_aquisicao"], '%Y-%m-%d').date()
        )
        cursor.execute(sql, values)
        conn.commit()
        imovel_id = cursor.lastrowid

        imovel_criado = {**data, "id": imovel_id}
        return format_imovel(imovel_criado), 201
    finally:
        cursor.close()
        conn.close()


def get_imovel_por_tipo(tipo):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
        results = cursor.fetchall()

        if not results:
            return {"erro": "Nenhum Imóvel encontrado"}, 404

        return [format_imovel(r) for r in results], 200
    finally:
        cursor.close()
        conn.close()


def get_imovel_por_cidade(cidade):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
        results = cursor.fetchall()

        if not results:
            return {"erro": "Nenhum Imóvel encontrado"}, 404

        return [format_imovel(r) for r in results], 200
    finally:
        cursor.close()
        conn.close()


def get_imovel(id):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            return {"erro": "Imóvel não encontrado"}, 404

        return format_imovel(result), 200
    finally:
        cursor.close()
        conn.close()


def get_data():
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM imoveis")
        results = cursor.fetchall()

        if not results:
            return {"erro": "Nenhum Imóvel encontrado"}, 404

        return [format_imovel(r) for r in results], 200
    finally:
        cursor.close()
        conn.close()


def delete_imovel(id):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
        result = cursor.fetchone()
        if not result:
            return {"erro": "Imóvel não encontrado"}, 404

        cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
        conn.commit()
        return {"mensagem": "Imóvel deletado com sucesso", "id": id}, 200
    finally:
        cursor.close()
        conn.close()


def editar_imovel(id, data):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
        result = cursor.fetchone()
        if not result:
            return {"erro": "Imóvel não encontrado"}, 404

        required_fields = ("logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao")
        if not data or not isinstance(data, dict) or not all(field in data for field in required_fields):
            return {"erro": "Dados inválidos ou incompletos"}, 400

        if not isinstance(data["valor"], (int, float)) or data["valor"] <= 0:
            return {"erro": "Dados inválidos ou incompletos"}, 400

        try:
            datetime.strptime(data["data_aquisicao"], "%Y-%m-%d")
        except Exception:
            return {"erro": "Dados inválidos ou incompletos"}, 400

        sql = """UPDATE imoveis 
                 SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s
                 WHERE id = %s"""
        values = (
            data["logradouro"], data["tipo_logradouro"], data["bairro"], data["cidade"],
            data["cep"], data["tipo"], data["valor"],
            datetime.strptime(data["data_aquisicao"], '%Y-%m-%d').date(),
            id
        )
        cursor.execute(sql, values)
        conn.commit()

        atualizado = {**data, "id": id}
        return format_imovel(atualizado), 200
    finally:
        cursor.close()
        conn.close()
