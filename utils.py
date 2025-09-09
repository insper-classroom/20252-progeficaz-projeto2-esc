from datetime import datetime


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
        resp = {"erro": "Nenhum aluno encontrado"}
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