from datetime import datetime

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
        data_aquisicao = datetime.strptime(data["data_aquisicao"], "%Y-%m-%d").date()
    except Exception:
        return {"erro": "Dados inválidos ou incompletos"}, 400
    
    cursor = conn.cursor()
    
    try:
        sql = """INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            data.get("logradouro"),
            data.get("tipo_logradouro"),
            data.get("bairro"),
            data.get("cidade"),
            data.get("cep"),
            data.get("tipo"),
            data.get("valor"),
            datetime.strptime(data.get("data_aquisicao"), '%Y-%m-%d').date() if data.get("data_aquisicao") else None
        )
        cursor.execute(sql, values)
        conn.commit()
        return {"mensagem": "Imóvel criado com sucesso"}, 201
    finally:
        cursor.close()
        conn.close()
        
        
        
def get_imovel(id):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id= %s", (id,))
    result = cursor.fetchone()
    if not result:
        return {"erro": "Imóvel não encontrado"}, 404
    else:
        imovel_dict = [{
            "id": result[0]["id"],
            "logradouro": result[0]["logradouro"],
            "tipo_logradouro": result[0]["tipo_logradouro"],
            "bairro": result[0]["bairro"],
            "cidade": result[0]["cidade"],
            "cep": result[0]["cep"],
            "tipo": result[0]["tipo"],
            "valor": float(result[0]["valor"]),
            "data_aquisicao": result[0]["data_aquisicao"]
        }]
        return imovel_dict, 200

def get_data():
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    cursor = conn.cursor()
    sql = "SELECT * FROM imoveis"
    cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum Imóvel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for i in results:
            imoveis_dict = {
                "id": i[0],
                "logradouro": i[1],
                "tipo_logradouro": i[2],
                "bairro": i[3],
                "cidade": i[4],
                "cep": i[5],
                "tipo": i[6],
                "valor": float(i[7]),
                "data_aquisicao": i[8]
            }
            imoveis.append(imoveis_dict)
        resp = imoveis
        return resp, 200
    
def delete_imovel(id):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id= %s", (id,))
    result = cursor.fetchone()
    if not result:
        return {"erro": "Imóvel não encontrado"}, 404
    else:
        cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
        conn.commit()
        return {"mensagem": "Imóvel deletado com sucesso"}, 200