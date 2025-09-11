from datetime import datetime


def get_imovel(id):
    from servidor import connect_db
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id= ?", (id,))
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