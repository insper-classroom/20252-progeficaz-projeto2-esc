from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from utils import get_data
app = Flask(__name__)
load_dotenv('.cred')


config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'imoveisdb'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}
def connect_db():
    return None 


@app.route('/imoveis', methods=['GET'])
def imoveis():
    resp, status = get_data()
    return resp, status

# @app.route('/imoveis/<int:id>', methods=['GET'])
# def imovel_detail(id):
#     conn = connect_db()
#     if conn is None:
#         return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
#     cursor = conn.cursor()
#     sql = "SELECT * FROM imoveis WHERE id = %s"
#     cursor.execute(sql, (id,))
#     result = cursor.fetchone()
#     if not result:
#         return {"erro": "Imóvel não encontrado"}, 404
#     else:
#         imovel_dict = {
#             "id": result[0],
#             "logradouro": result[1],
#             "tipo_logradouro": result[2],
#             "bairro": result[3],
#             "cidade": result[4],
#             "cep": result[5],
#             "tipo": result[6],
#             "valor": float(result[7]),
#             "data_aquisicao": result[8]
#         }
#         return imovel_dict, 200


if __name__ == "__main__":
    app.run(debug=True)