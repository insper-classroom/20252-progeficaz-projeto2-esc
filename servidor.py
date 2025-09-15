from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from utils import get_data, get_imovel,novo_imovel,delete_imovel,editar_imovel,get_imovel_por_tipo,get_imovel_por_cidade
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
    resp, status = get_imovel(id)
    return resp, status

@app.route('/imoveis', methods=['POST'])
def criar_imoveis():
    data = request.get_json()
    resp, status = novo_imovel(data)
    return resp, status

@app.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    resp, status = delete_imovel(id)
    return resp, status

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    data = request.get_json()
    resp, status = editar_imovel(id, data)
    return resp, status

@app.route('/imoveis/tipo/<string:tipo>', methods=['GET'])
def imoveis_por_tipo(tipo):
    resp, status = get_imovel_por_tipo(tipo)
    return resp, status

@app.route('/imoveis/cidade/<string:cidade>', methods=['GET'])
def imoveis_por_cidade(cidade):
    resp, status = get_imovel_por_cidade(cidade)
    return resp, status



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)