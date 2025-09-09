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
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


@app.route('/imoveis', methods=['GET'])
def imoveis():
    resp, status = get_data()
    return resp, status

@app.route('/imoveis/<int:id>', methods=['GET'])
def imovel_detail(id):
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id= ?", (id,))
    result = cursor.fetchone()
    # print(result[0]["id"])
    # print(result[0]["logradouro"])
    # print(result[0]["tipo_logradouro"])
    # print(result[0]["bairro"])
    # print(result[0]["tipo"])
    # print()
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


if __name__ == "__main__":
    app.run(debug=True)